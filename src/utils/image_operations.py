from enum import Enum
import numpy as np
import cv2


class InterpolationMethod(Enum):
    BILINEAR = "bilinear"
    BICUBIC = "bicubic"
    AVERAGE = "average"


def bilinear_interpolation(image, x, y):
    """
    Bilinear interpolasyon uygular.

    Args:
        image: Görüntü matrisi
        x: x koordinatı
        y: y koordinatı

    Returns:
        İnterpolasyon sonucu piksel değeri
    """
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, image.shape[1] - 1), min(y1 + 1, image.shape[0] - 1)

    # Sınırları kontrol et
    if x1 >= image.shape[1] - 1 or y1 >= image.shape[0] - 1:
        return image[y1, x1]

    # Ağırlıkları hesapla
    wx = x - x1
    wy = y - y1

    # Dört komşu pikselin değerlerini al
    p1 = image[y1, x1]
    p2 = image[y1, x2]
    p3 = image[y2, x1]
    p4 = image[y2, x2]

    # Bilinear interpolasyon formülü
    result = (
        (1 - wx) * (1 - wy) * p1
        + wx * (1 - wy) * p2
        + (1 - wx) * wy * p3
        + wx * wy * p4
    )

    return result.astype(np.uint8)


def bicubic_interpolation(image, x, y):
    """
    Bicubic interpolasyon uygular.

    Args:
        image: Görüntü matrisi
        x: x koordinatı
        y: y koordinatı

    Returns:
        İnterpolasyon sonucu piksel değeri
    """
    x1, y1 = int(x), int(y)

    # 4x4 komşuluk matrisi için sınırları kontrol et
    if x1 < 1 or y1 < 1 or x1 >= image.shape[1] - 2 or y1 >= image.shape[0] - 2:
        return bilinear_interpolation(image, x, y)

    # 4x4 komşuluk matrisini al
    neighborhood = image[y1 - 1 : y1 + 3, x1 - 1 : x1 + 3]

    # Bicubic kernel fonksiyonu
    def cubic_kernel(x):
        a = -0.5
        if abs(x) <= 1:
            return (a + 2) * abs(x) ** 3 - (a + 3) * abs(x) ** 2 + 1
        elif abs(x) < 2:
            return a * abs(x) ** 3 - 5 * a * abs(x) ** 2 + 8 * a * abs(x) - 4 * a
        return 0

    # x ve y için ağırlıkları hesapla
    wx = x - x1
    wy = y - y1

    # 4x4 matris için ağırlıkları hesapla
    weights_x = np.array([cubic_kernel(wx + i) for i in range(-1, 3)])
    weights_y = np.array([cubic_kernel(wy + i) for i in range(-1, 3)])

    # Her kanal için interpolasyon uygula
    result = np.zeros(3, dtype=np.float32)
    for c in range(3):
        channel = neighborhood[:, :, c]
        temp = np.zeros((4, 4), dtype=np.float32)
        for i in range(4):
            for j in range(4):
                temp[i, j] = channel[i, j] * weights_x[j] * weights_y[i]
        result[c] = np.sum(temp)

    return np.clip(result, 0, 255).astype(np.uint8)


def average_interpolation(image, x, y):
    """
    Ortalama interpolasyon uygular.

    Args:
        image: Görüntü matrisi
        x: x koordinatı
        y: y koordinatı

    Returns:
        İnterpolasyon sonucu piksel değeri
    """
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, image.shape[1] - 1), min(y1 + 1, image.shape[0] - 1)

    # Sınırları kontrol et
    if x1 >= image.shape[1] - 1 or y1 >= image.shape[0] - 1:
        return image[y1, x1]

    # Dört komşu pikselin değerlerini al ve ortalamasını hesapla
    p1 = image[y1, x1]
    p2 = image[y1, x2]
    p3 = image[y2, x1]
    p4 = image[y2, x2]

    return np.mean([p1, p2, p3, p4], axis=0).astype(np.uint8)


def resize_image(image, scale, interpolation_method=InterpolationMethod.BILINEAR):
    """
    Görüntüyü yeniden boyutlandırır.

    Args:
        image: Görüntü matrisi
        scale: Ölçek faktörü
        interpolation_method: İnterpolasyon yöntemi

    Returns:
        Yeniden boyutlandırılmış görüntü
    """
    height, width = image.shape[:2]
    new_height = int(height * scale)
    new_width = int(width * scale)

    result = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for y in range(new_height):
        for x in range(new_width):
            # Orijinal görüntüdeki karşılık gelen koordinatları hesapla
            orig_x = x / scale
            orig_y = y / scale

            # Seçilen interpolasyon yöntemini uygula
            if interpolation_method == InterpolationMethod.BILINEAR:
                result[y, x] = bilinear_interpolation(image, orig_x, orig_y)
            elif interpolation_method == InterpolationMethod.BICUBIC:
                result[y, x] = bicubic_interpolation(image, orig_x, orig_y)
            else:  # AVERAGE
                result[y, x] = average_interpolation(image, orig_x, orig_y)

    return result


def rotate_image(image, angle, interpolation_method=InterpolationMethod.BILINEAR):
    """
    Görüntüyü döndürür.

    Args:
        image: Görüntü matrisi
        angle: Döndürme açısı (derece)
        interpolation_method: İnterpolasyon yöntemi

    Returns:
        Döndürülmüş görüntü
    """
    height, width = image.shape[:2]

    # Döndürme matrisini hesapla
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Yeni boyutları hesapla
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))

    # Döndürme matrisini güncelle
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    result = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Ters dönüşüm matrisini hesapla
    inv_rotation_matrix = cv2.invertAffineTransform(rotation_matrix)

    for y in range(new_height):
        for x in range(new_width):
            # Orijinal görüntüdeki karşılık gelen koordinatları hesapla
            orig_x = (
                inv_rotation_matrix[0, 0] * x
                + inv_rotation_matrix[0, 1] * y
                + inv_rotation_matrix[0, 2]
            )
            orig_y = (
                inv_rotation_matrix[1, 0] * x
                + inv_rotation_matrix[1, 1] * y
                + inv_rotation_matrix[1, 2]
            )

            # Koordinatlar görüntü sınırları içinde mi kontrol et
            if 0 <= orig_x < width and 0 <= orig_y < height:
                # Seçilen interpolasyon yöntemini uygula
                if interpolation_method == InterpolationMethod.BILINEAR:
                    result[y, x] = bilinear_interpolation(image, orig_x, orig_y)
                elif interpolation_method == InterpolationMethod.BICUBIC:
                    result[y, x] = bicubic_interpolation(image, orig_x, orig_y)
                else:  # AVERAGE
                    result[y, x] = average_interpolation(image, orig_x, orig_y)

    return result


def zoom_image(image, zoom_factor, interpolation_method=InterpolationMethod.BILINEAR):
    """
    Görüntüyü yakınlaştırır veya uzaklaştırır.

    Args:
        image: Görüntü matrisi
        zoom_factor: Yakınlaştırma faktörü
        interpolation_method: İnterpolasyon yöntemi

    Returns:
        Yakınlaştırılmış/uzaklaştırılmış görüntü
    """
    height, width = image.shape[:2]

    # Merkez noktası
    center_x = width / 2
    center_y = height / 2

    # Yeni boyutları hesapla
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)

    result = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for y in range(new_height):
        for x in range(new_width):
            # Orijinal görüntüdeki karşılık gelen koordinatları hesapla
            orig_x = (x - new_width / 2) / zoom_factor + center_x
            orig_y = (y - new_height / 2) / zoom_factor + center_y

            # Koordinatlar görüntü sınırları içinde mi kontrol et
            if 0 <= orig_x < width and 0 <= orig_y < height:
                # Seçilen interpolasyon yöntemini uygula
                if interpolation_method == InterpolationMethod.BILINEAR:
                    result[y, x] = bilinear_interpolation(image, orig_x, orig_y)
                elif interpolation_method == InterpolationMethod.BICUBIC:
                    result[y, x] = bicubic_interpolation(image, orig_x, orig_y)
                else:  # AVERAGE
                    result[y, x] = average_interpolation(image, orig_x, orig_y)

    return result
