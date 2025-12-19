 self.bg_img = self.resource_manager.get_image("clan_four_light")
        self.bg_rect = self.bg_img.get_rect() if self.bg_img else None
        
        self.frame_img = self.resource_manager.get_image("clan_name_frame")
        self.frame_rect = self.frame_img.get_rect() if self.frame_img else None
        
        self.frame_img_bg = self.resource_manager.get_image("basic_frame")
        self.frame_bg_rect = self.frame_img_bg.get_rect() if self.frame_img_bg else None