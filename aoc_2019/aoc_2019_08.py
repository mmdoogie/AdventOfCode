from mrm.image import make_image, ocr_image
def parse():
    with open('data/aoc_2019/08.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    width = 25
    height = 6
    layer_size = width * height
    layer_count = len(dat[0]) // layer_size

    layers = [dat[0][layer_size*i:layer_size*(i + 1)] for i in range(layer_count)]

    return layers, width, height

def part1(output=False):
    layers, _, _ = parse()

    zero_cnt = [sum([c == '0' for c in l]) for l in layers]
    ones_cnt = [sum([c == '1' for c in l]) for l in layers]
    twos_cnt = [sum([c == '2' for c in l]) for l in layers]

    tgt_layer = zero_cnt.index(min(zero_cnt))

    return ones_cnt[tgt_layer] * twos_cnt[tgt_layer]

def part2(output=False):
    layers, width, height = parse()
    layer_size = width * height

    pixel_layers = [[l[i] != '2' for l in layers].index(True) for i in range(layer_size)]
    output_pixels = [layers[pixel_layers[i]][i] for i in range(layer_size)]

    present = {(x, y): True for y in range(height) for x in range(width) if output_pixels[width*y+x] == '1'}
    img = make_image(present, output)
    return ocr_image(img)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
