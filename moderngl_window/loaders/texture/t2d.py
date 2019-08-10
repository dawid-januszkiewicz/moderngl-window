import logging

from moderngl_window.loaders.texture.pillow import PillowLoader, image_data

logger = logging.getLogger(__name__)


class Loader(PillowLoader):
    kind = '2d'

    def load(self):
        """Load a 2d texture"""
        self._open_image()

        # Handle images with palettes
        if self.image.palette and self.image.palette.mode == 'RGB':
            logger.debug("Converting P image to RGB using palette")
            self.image = self.image.convert('RGB', palette=self.image.palette)

        components, data = image_data(self.image)

        texture = self.ctx.texture(
            self.image.size,
            components,
            data,
        )
        texture.extra = {'meta': self.meta}

        if self.meta.mipmap_levels is not None:
            self.meta.mipmap = True

        if self.meta.mipmap:
            if isinstance(self.meta.mipmap_levels, tuple):
                texture.build_mipmaps(*self.meta.mipmap_levels)
            else:
                texture.build_mipmaps()

            if self.meta.anisotropy:
                texture.anisotropy = self.meta.anisotropy

        self._close_image()

        return texture
