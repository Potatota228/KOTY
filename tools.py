def scale_with_aspect_ratio(image, target_size):
    """Масштабирует изображение с сохранением пропорций"""
    image_rect = image.get_rect()
    target_rect = pg.Rect(0, 0, *target_size)
    
    # Вычисляем масштаб
    scale = max(
        target_rect.width / image_rect.width,
        target_rect.height / image_rect.height
    )
    
    new_size = (
        int(image_rect.width * scale),
        int(image_rect.height * scale)
    )
    
    return pg.transform.scale(image, new_size)