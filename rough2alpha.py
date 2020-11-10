"""
Rough2Alpha
"""
import argparse
from PIL import Image, ImageOps

def convert(target_file, source_file, suffix='AlphaRough'):
    source_img = Image.open(source_file).convert('RGB')
    target_img = Image.open(target_file).convert('RGB')

    if source_img.size != target_img.size:
        raise Exception('Texture images have different dimensions')

    # Invert the image colors
    source_inverted = ImageOps.invert(source_img)

    # We should convert in L image mode before injecting it as the alpha channel
    source_inverted = source_inverted.convert('L')
    source_inverted.save('inverted.jpg')

    filename, ext = target_file.split('.')

    # Make sure we don't use jpg as it doesn't support alpha channel
    ext = 'png' if ext == 'jpg' else ext

    target_img.putalpha(source_inverted)
    target_img.save('%s_%s.%s' % (target_file.split('.')[0], suffix, ext))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Converts a Roughness texture to a Smoothness one, and inject it as the alpha channel
        of a Albedo or Metallic texture, so you can use it (for example) with Unity and its metallic PBR workflow.
        You may use any image format as long as they support an alpha channel.
    """)
    parser.add_argument('source', help='Source file, should be a Roughness texture')
    parser.add_argument('target', help='Target file, should be a Albedo (Color) or Metalness texture')
    parser.add_argument('--suffix', help='Suffix added to the new texture file name', default='AlphaRough')
    args = parser.parse_args()

    print("Converting your texture...")
    convert(args.target, args.source, args.suffix)
    print("Done !")
