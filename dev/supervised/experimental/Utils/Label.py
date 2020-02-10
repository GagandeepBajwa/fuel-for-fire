from Utils.Misc import *
from Utils.DataManip import *

class Label(object):
    def __init__(self, name, bin, cfg):
        self.name = name
        s,l,b,self.Data = read_binary(bin)
        self.samples, self.lines, self.bands = int(s), int(l), int(b)
        self.__build_binary(cfg)

    def __build_binary(self, cfg):
        classes = cfg['bcgw_labels']
        if self.name in classes:
            bstr = classes[self.name]['bool']
            val =  classes[self.name]['val']

            if bstr == 'True':
                self.Binary = self.Data == float(val)
            elif bstr == 'False':
                self.Binary = self.Data != float(val)
            else:
                raise Exception('There was an error encoding binaries')

    def ravel(self, binary=True):
        if binary:
            return self.Binary.reshape(self.lines * self.samples)
        else:
            return self.Data.reshape(self.lines *  self.samples)

    def spatial(self, binary=True):
        if binary:
            return self.Binary.reshape(self.lines, self.samples)
        else:
            return self.Data.reshape(self.lines, self.samples)

    def showplot(self, binary=True):
<<<<<<< HEAD
        y = self.spatial(binary=binary)
        if binary:
            plt.imshow(y, cmap='gray')
        else:
            plt.imshow(y)
=======
        if binary:
            plt.imshow(self.spatial(binary=binary), cmap='gray')
        else:
            plt.imshow(self.spatial(binary=binary))
>>>>>>> 376351d262e8c6339e557797f18e673f8584f5e2
        plt.tight_layout()
        plt.show()