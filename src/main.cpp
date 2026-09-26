#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    std::cout << "=== ZINO AgroVision Engine v2.0 (Advanced Visual Diagnostic) ===" << std::endl;
    
    // 1. Load image
    cv::Mat img = cv::imread("../images/test_leaf.jpg");
    if (img.empty()) {
        std::cerr << "Error: Could not load image!" << std::endl;
        return -1;
    }
    std::cout << "[System] Image Loaded: " << img.cols << "x" << img.rows << " px" << std::endl;

    // Convert to HSV
    cv::Mat hsv;
    cv::cvtColor(img, hsv, cv::COLOR_BGR2HSV);

    // 2. Leaf Masking (Isolate leaf structure from non-plant background)
    cv::Mat leaf_mask;
    cv::inRange(hsv, cv::Scalar(10, 30, 30), cv::Scalar(95, 255, 255), leaf_mask);

    int total_leaf_pixels = cv::countNonZero(leaf_mask);
    if (total_leaf_pixels == 0) {
        std::cout << "[Warning] No leaf structure detected!" << std::endl;
        return 0;
    }

    // 3. Healthy vs Diseased Segmentation within Leaf Area
    cv::Mat healthy_mask, diseased_mask;
    cv::inRange(hsv, cv::Scalar(35, 40, 40), cv::Scalar(85, 255, 255), healthy_mask);
    
    // Restrict analysis inside the leaf boundaries only
    cv::bitwise_and(healthy_mask, leaf_mask, healthy_mask);
    cv::bitwise_xor(leaf_mask, healthy_mask, diseased_mask);

    int healthy_pixels = cv::countNonZero(healthy_mask);
    int diseased_pixels = cv::countNonZero(diseased_mask);

    double healthy_ratio = (double)healthy_pixels / total_leaf_pixels * 100.0;
    double disease_severity = (double)diseased_pixels / total_leaf_pixels * 100.0;

    // 4. Output Diagnostic Report
    std::cout << "\n============ DIAGNOSTIC REPORT ============" << std::endl;
    std::cout << "Total Leaf Area:   " << total_leaf_pixels << " pixels" << std::endl;
    std::cout << "Healthy Tissue:    " << healthy_ratio << " %" << std::endl;
    std::cout << "Disease Severity:  " << disease_severity << " %" << std::endl;
    std::cout << "-------------------------------------------" << std::endl;

    if (disease_severity < 15.0) {
        std::cout << "Diagnosis Status: HEALTHY / MINIMAL STRESS" << std::endl;
    } else if (disease_severity < 40.0) {
        std::cout << "Diagnosis Status: MODERATE DISEASE / NUTRIENT STRESS" << std::endl;
    } else {
        std::cout << "Diagnosis Status: SEVERE PATHOGEN INFECTION!" << std::endl;
    }
    std::cout << "===========================================\n" << std::endl;

    // 5. Annotate diseased zones with Red highlights and save output image
    cv::Mat output_img = img.clone();
    output_img.setTo(cv::Scalar(0, 0, 255), diseased_mask);
    
    cv::imwrite("../images/output_analyzed.jpg", output_img);
    std::cout << "[IO] Diagnostic visual output saved: images/output_analyzed.jpg" << std::endl;

    return 0;
}
