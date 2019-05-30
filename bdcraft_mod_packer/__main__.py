import argparse
import os

from bdcraft_mod_packer import default_config, default_url
from bdcraft_mod_packer import packer, downloader
from bdcraft_mod_packer.web_parser import parse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--mc-version', help='The latest supported mc version by texture pack',
                            default=default_config['mc_version'])
    arg_parser.add_argument('-o', '--output', help='The zip output dir', default=default_config['output_dir'])
    arg_parser.add_argument('-res', '--resolution', help='The resolution you need. Such as 64x, 128x.'
                                                         'If a texture pack don\'t have the resolution,'
                                                         'the pack will not be included.',
                            default=default_config['resolution'])
    args = arg_parser.parse_args()
    resolution = args.resolution
    mc_version = args.mc_version
    output_path = args.output

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    root_html: str = downloader.download_html(default_url)
    zip_urls = parse(root_html, mc_version, resolution)

    with open(os.path.join(output_path, 'zip_urls.txt'), 'w') as f:
        for zip_url in zip_urls:
            f.write(zip_url + '\n')

    for zip_url in zip_urls:
        downloader.download_zip(zip_url.strip(), output_path)

    packer.pack(output_path)


if __name__ == '__main__':
    main()
