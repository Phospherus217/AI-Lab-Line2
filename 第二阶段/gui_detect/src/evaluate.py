from config import IOU_THRESHOLD

def box_iou(box_a, box_b):
    """
    算两个框的 IoU，输入都是 [x1, y1, x2, y2]。
    IoU = 交集面积 / 并集面积
    """
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    # 交集的左上角：取两个框左边界、上边界的较大值
    intersection_x1 = max(ax1, bx1)
    intersection_y1 = max(ay1, by1)
    # 交集的右下角：取两个框右边界、下边界的较小值
    intersection_x2 = min(ax2, bx2)
    intersection_y2 = min(ay2, by2)
    # 两个框不相交时，上面的差会是负数，用 0 截断
    intersection_width = max(0.0, intersection_x2 - intersection_x1)
    intersection_height = max(0.0, intersection_y2 - intersection_y1)
    intersection_area = intersection_width * intersection_height

    # 各自面积
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    # 并集 = A + B - 交集（交集被算了两遍，要减掉一次）
    union_area = area_a + area_b - intersection_area
    # 防止除零
    if union_area <= 0:
        return 0.0
    return intersection_area / union_area

def match_boxes(predicted_boxes, ground_truth_boxes,iou_threshold=IOU_THRESHOLD):
    """贪心匹配预测框和真实框，返回 (正确数, 误报数, 漏检数, 匹配对)。

     规则：
       1. 每轮找 IoU 最大的一对
       2. IoU 超过阈值 → 算正确，两边都标记为已用
       3. 剩下的预测框 → 误报
       4. 剩下的真实框 → 漏检
     """
    # 两个布尔列表，记录"这个框是否已经配对过"
    # 列表乘法
    used_ground_truth = [False] * len(ground_truth_boxes)
    used_prediction = [False] * len(predicted_boxes)
    correct_count = 0        # 正确匹配数（TP）
    matched_pairs = []       # 记录匹配对，方便调试

    # 每轮找一对最优匹配，直到找不到为止
    while True:
        best_iou = 0.0
        best_prediction_index = -1
        best_ground_truth_index = -1

        # 双重循环：所有"未配对预测 × 未配对真实"
        for prediction_index, prediction in enumerate(predicted_boxes):
            if used_prediction[prediction_index]:
                continue
            for ground_truth_index, ground_truth in enumerate(ground_truth_boxes):
                if used_ground_truth[ground_truth_index]:
                    continue

                iou = box_iou(prediction["box"], ground_truth["box"])

                # 只保留当前最大的一对
                if iou > best_iou:
                    best_iou = iou
                    best_prediction_index = prediction_index
                    best_ground_truth_index = ground_truth_index

        # 一个都配不上，或最大 IoU 也不够阈值 → 结束
        if best_prediction_index == -1 or best_iou < iou_threshold:
            break

        # 标记已用，计数 +1
        used_prediction[best_prediction_index] = True
        used_ground_truth[best_ground_truth_index] = True
        correct_count += 1
        matched_pairs.append((best_prediction_index, best_ground_truth_index, best_iou))

    # 剩下没配上的预测框 = 误报；剩下没配上的真实框 = 漏检
    false_positive_count = sum(1 for used in used_prediction if not used)
    false_negative_count = sum(1 for used in used_ground_truth if not used)

    return correct_count, false_positive_count, false_negative_count, matched_pairs

def precision_recall(correct_count, false_positive_count, false_negative_count):
    """算精确率和召回率，分母为 0 时返回 0。"""
    # 精确率 = 报对的 / 报出来的总数
    precision = (correct_count / (correct_count + false_positive_count)
                 if (correct_count + false_positive_count) > 0 else 0.0)

    # 召回率 = 报对的 / 真实目标总数
    recall = (correct_count / (correct_count + false_negative_count)
              if (correct_count + false_negative_count) > 0 else 0.0)

    return precision, recall

def evaluate_one(predicted_boxes, ground_truth_boxes, iou_threshold=0.5):
    """对一张图算出完整指标，返回字典。"""
    # 先配对
    correct_count, false_positive_count, false_negative_count, matched_pairs = match_boxes(
        predicted_boxes, ground_truth_boxes, iou_threshold)

    # 再算精确率、召回率
    precision, recall = precision_recall(
        correct_count, false_positive_count, false_negative_count)

    # 统一返回一个字典，方便写进 CSV
    return {
        "correct_count": correct_count,
        "false_positive_count": false_positive_count,
        "false_negative_count": false_negative_count,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "ground_truth_count": len(ground_truth_boxes),
        "prediction_count": len(predicted_boxes),
    }