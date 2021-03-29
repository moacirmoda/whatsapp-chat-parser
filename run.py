import argparse
from parser import generate_report_from_android


parser = argparse.ArgumentParser(description='Whatsapp Chat Parser')
parser.add_argument(
    '-d', 
    '--directory',
    required=True,
    help='Diretório onde estão os arquivos'
)

parser.add_argument(
    '-s',
    '--source',
    default='android',
    help='Oirgem de onde veio o chat. Padrão = Android'
)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.source == 'android':
        generate_report_from_android(args.directory)
