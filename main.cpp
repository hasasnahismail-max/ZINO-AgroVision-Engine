#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    std::cout << "=== ZINO AgroVision Engine Initialized ===" << std::endl;

    // Path to the test leaf image
    std::string imagePath = "../images/test_leaf.jpg";
    cv::Mat img = cv::imread(imagePath);

    if (img.empty()) {
        std::cerr << "Error: Image not found at path: " << imagePath << std::endl;
        std::cerr << "Please upload a leaf image named test_leaf.jpg inside the images folder." << std::endl;
        return -1;
    }

    std::cout << "Image loaded successfully! Dimensions: " << img.cols << "x" << img.rows << std::endl;

    return 0;
}
