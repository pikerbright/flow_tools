from PIL import Image
import numpy as np
import os

def get_flow(filename, index, type):
    imgx = Image.open(filename + 'flow_x_{:0>5d}.{}'.format(index, type))
    imgy = Image.open(filename + 'flow_y_{:0>5d}.{}'.format(index, type))
    imgx = np.array(imgx, dtype=np.float) - 128
    imgy = np.array(imgy, dtype=np.float) - 128
    flow = np.stack([imgx, imgy], 2)


def get_file_name():
    with open('kinetics_all.log') as f:
        for line in f:
            class_name = line.split('.mp4')[0].split('/')[-2]
            file_name = line.split('.mp4')[0].split('/')[-1]+'.mp4'
            yield file_name, class_name


def get_flow_pic(file_name):
    with open('d.conf', 'w') as f:
        conf = '{\n' + \
	           '"dest_dir"	:	".",\n' + \
	           '"bucket"	:	"dataset-kinetics",\n' + \
	           '"prefix"	:	"resized-kinetics-flows/{}"\n'.format(file_name) + \
                '}\n'
        f.write(conf)
        print(conf)

    os.system('qshell qdownload 50 d.conf')

def clean():
    cmd = "rm -r resized-kinetics-flows"
    os.system(cmd)

def check_flow(file_name, class_name):
    cmd = "ls -l resized-kinetics-flows/{} | wc -l".format(file_name)
    f = os.popen(cmd)
    num = int(f.read())
    num = int((num - 1)/2)
    file_type = 'jpg'
    p_list = []
    n_list = []
    for index in range(num):
        imgx = Image.open('resized-kinetics-flows/' + file_name + '/flow_x_{:0>5d}.{}'.format(index+1, file_type))
        imgy = Image.open('resized-kinetics-flows/' + file_name + '/flow_y_{:0>5d}.{}'.format(index+1, file_type))
        imgx = np.array(imgx, dtype=np.float) - 128
        imgy = np.array(imgy, dtype=np.float) - 128
        shape = imgx.shape
        flow = np.stack([imgx, imgy], 2)
        radm = np.mean(np.sqrt(imgx*imgx + imgy*imgy))

    flow_p_mean = np.mean(p_list)
    flow_n_mean = np.mean(n_list)

    if num:
        print(flow_p_mean, flow_n_mean)
        with open('check_flow_result.txt', 'a') as f:
            s = "{}/{}: {}: {}: {}\n".format(class_name, file_name, flow_p_mean, flow_n_mean, shape)
            f.write(s)


if __name__ == "__main__":
    for file_name, class_name in get_file_name():
        print(file_name)
        get_flow_pic(file_name)
        check_flow(file_name, class_name)
        # clean()
