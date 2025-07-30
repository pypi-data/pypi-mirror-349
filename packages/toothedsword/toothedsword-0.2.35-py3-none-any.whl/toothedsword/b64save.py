import numpy as np
import json
import base64
from io import BytesIO
import re
import os

def dict2b64(data):
    if str(type(data)) == str(type({0:1})):
        ks = list(data.keys())
        for k in ks:
            if str(type(data[k])) == str(type(np.array([0,1]))):
                b = base64.b64encode(data[k])
                sb = str(b)[2:-1]+'|numpy'
                data[k+'_type'] = str(data[k].dtype)
                data[k+'_shape'] = data[k].shape
                data[k] = sb
            else:
                dict2b64(data[k])
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            dict2b64(data[k])
    else:
        return


def dict2numpy(data, file, name):
    if str(type(data)) == str(type({0:1})):
        ks = list(data.keys())
        for k in ks:
            if str(type(data[k])) == str(type(np.array([0,1]))):
                outdir = file+'.data/'
                if ~os.path.exists(outdir):
                    os.system('mkdir -p '+outdir)
                b = name+'.'+k+'.npy'
                np.save(outdir+b, data[k])
                data[k] = b
            else:
                dict2numpy(data[k],file,name+'.'+str(k))
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            dict2numpy(data[k],file,name+'.'+str(k))
    else:
        return


def b642dict(data):
    if str(type(data)) == str(type({0:1})):
        for k in data.keys():
            if str(type(data[k])) == str(type('s')):
                if re.search(r'\|numpy$', data[k]):
                    b = base64.decodebytes(bytes(re.sub(r'\|.*','',data[k]), "utf8"))
                    data[k] = np.frombuffer(b, dtype=data[k+'_type']).reshape(data[k+'_shape'])
            else:
                b642dict(data[k])
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            b642dict(data[k])
    else:
        return


def numpy2dict(data,file,name=''):
    if str(type(data)) == str(type({0:1})):
        for k in data.keys():
            if str(type(data[k])) == str(type('s')):
                if re.search(r'\.npy$', data[k]):
                    if re.search(r'ALLDATA', name):
                        print(file+'.data/'+data[k])
                        data[k] = np.load(file+'.data/'+data[k])
                    else:
                        if re.search(r'0\.'+name+r'\.npy$', data[k]):
                            data[k] = np.load(file+'.data/'+data[k])
            else:
                numpy2dict(data[k],file,name)
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            numpy2dict(data[k],file,name)
    else:
        return


def dict2json(data, file):
    dict2b64(data)
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def dict2jsons(data, file):
    dict2numpy(data, file, '0')
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def json2dict(file):
    with open(file) as json_file:
        data = json.load(json_file)
    pass
    b642dict(data)
    return data 


def jsons2dict(file,name='ALLDATA'):
    with open(file) as json_file:
        data = json.load(json_file)
    pass
    if name == 'None':
        pass
    else:
        numpy2dict(data,file,name)
    return data 


def t1():
    dt = {}
    t = np.array([1,2,3], dtype=np.float32)
    t = np.arange(24).reshape(4, 3, 2).astype(np.float32)
    dt['t'] = t
    print(dt)
    dict2b64(dt) 
    print(dt)
    b642dict(dt)
    print(dt)


def test():
    t = {}
    t[1] = 1
    t[2] = np.array([0,1], dtype=np.float32)
    t[2] = np.arange(24).reshape(3, 4, 2).astype(np.float32)
    b = base64.b64encode(t[2])
    sb = str(b)
    data = base64.decodebytes(bytes(sb[2:-1], "utf8"))
    t1 = np.frombuffer(data, dtype=np.float32)
    print(t1)
    breakpoint()
    b64 = 'data:application/octet-stream;base64,'+str(b)[2:-1]
    t[2] = b64
    with open('t.json', "w", encoding='utf-8') as f:
        json.dump(t, f)
    exit()

# numpy数组转base64编码
    arr = np.arange(12).reshape(3, 4)
    bytesio = BytesIO()
    np.savetxt(bytesio, arr) # 只支持1维或者2维数组，numpy数组转化成字节流
    content = bytesio.getvalue()  # 获取string字符串表示
    print(content)
    b64_code = base64.b64encode(content)
     
# 从base64编码恢复numpy数组
    b64_decode = base64.b64decode(b64_code)
    arr = np.loadtxt(BytesIO(b64_decode))
    print(arr)
    breakpoint()


def main():
    # 数据
    dt = {}
    t = np.array([2,3], dtype=np.float32)
    t = np.arange(32).reshape(2, 2, 8).astype(np.int16)
    np.save('t.npy', t)
    dt['n'] = t
    dt['d'] = {1:4, 'a':'b'}
    dt['l'] = [1,2,3,'o']
    dt['n1'] = t+1
    import copy
    dt1 = copy.deepcopy(dt)

    # 将数据存为json
    dict2json(dt, 'dt.json')

    # 读取json数据
    dto = json2dict('dt.json')

    # 将数据存为json
    dict2jsons(dt1, 'dt1.json')

    # 读取json数据
    dto1 = jsons2dict('dt1.json', 'None')
    print(dto1)


if __name__ == "__main__":
    main()
