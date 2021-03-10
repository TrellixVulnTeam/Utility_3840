from termcolor import colored, cprint
import csv
import cv2 as cv
import numpy as np
import utility

class EAN13:
    '''
    EAN13 Barcode generator.

    Args:
        dat_folder (str): Path of the folder containing the csv files
                          needed to generate EAN13 barcode
    
    Attributes:
        __LEFT_ODD_FILE (str): Path of the csv file containing the Barcode
                               encoding for the first 6 digits, after the 
                               first one, when odd value

        __LEFT_EVEN_FILE (str): Path of the csv file containing the Barcode
                                encoding for the first 6 digits, after the 
                                first one, when even value

        __RIGHT_FILE (str): Path of the csv file containing the Barcode
                               encoding for the last 6 digits

        __FIRST_NUM_FILE (str): Path of the csv file containing the Barcode
                                encoding for the first 6 digits, after the
                                first one, in terms of odd and even values

        __FIRST_LAST (str): Encoding of opening and closing Braille bars

        __MIDDLE (str): Encoding of central Braille bars

        __UNIT_SIZE (int): Size of a unit in term of pixels

        __HORIZONTAL_QUIET_ZONE (int): Horizontal quiet zone size in terms
                                       of number of units

        __VERTICAL_QUIET_ZONE (int): Vertical quiet zone size in terms
                                     of number of units

        __BARCODE_HEIGHT (int): Height of the barcode bars in terms of 
                                number of units

        __HEIGHT_NUM (int): Height of the digits, under the barcode, in
                            terms of number of units
        
        __TOTAL_HEIGHT (int): Height of the image, including quiet zones,
                              in terms of number of pixels

        __TOTAL_WIDTH (int): Width of the image, including quiet zones,
                             in terms of number of pixels

        __FIRST_NUM_CODES (dict): Barcode scheme for the first 6 digits, 
                                  after the first one, looking to the
                                  first digit

        __LEFT_ODD_CODES (dict): Barcode encodings for the digits alphabeth for 
                                 the first 6 digits, after the first one, when 
                                 odd values

        __LEFT_EVEN_CODES (dict): Barcode encodings for the digits alphabeth for 
                                  the first 6 digits, after the first one, when 
                                  even values

        __RIGHT_CODES (dict): Barcode encodings for the digits alphabeth for 
                              the last 6 digits

    '''
    
    __LEFT_ODD_FILE = 'left_odd.csv'
    __LEFT_EVEN_FILE = 'left_odd.csv'
    __RIGHT_FILE = 'right.csv'
    __FIRST_NUM_FILE = 'first_num.csv'
    __FIRST_LAST = '101'
    __MIDDLE = '01010'

    #Size of a unit in pixel
    __UNIT_SIZE = 2
    #Size in units
    __HORIZONTAL_QUIET_ZONE = 10
    __VERTICAL_QUIET_ZONE = 10
    __BARCODE_HEIGHT = 50
    __HEIGHT_NUM = 10
    __TOTAL_HEIGHT = (__VERTICAL_QUIET_ZONE*2+__BARCODE_HEIGHT+__HEIGHT_NUM)*__UNIT_SIZE

    __TOTAL_WIDTH = (7*12+11+__HORIZONTAL_QUIET_ZONE*2)*__UNIT_SIZE

    __FIRST_NUM_CODES = {}
    __LEFT_ODD_CODES = {}
    __LEFT_EVEN_CODES = {}
    __RIGHT_CODES = {}

    def __init__(self, dat_folder='../dat/EAN13/'):
        dat_folder = utility.uniform_dir_path(dat_folder)

        with open(dat_folder+self.__LEFT_ODD_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__LEFT_ODD_CODES[row[0]] = row[1]

        with open(dat_folder+self.__LEFT_EVEN_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__LEFT_EVEN_CODES[row[0]] = row[1]

        with open(dat_folder+self.__RIGHT_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__RIGHT_CODES[row[0]] = row[1]

        with open(dat_folder+self.__FIRST_NUM_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__FIRST_NUM_CODES[row[0]] = row[1:]

    def encode(self, code):
        if len(code) != 13 or not code.isnumeric():
            print('Invalid number', end='\n\n')
            return
        else:
            self.create_barcode(code)
            cprint('Completed encoding', 'yellow', end='\n\n')

    def create_barcode(self, code):
        img = np.zeros((self.__TOTAL_HEIGHT, self.__TOTAL_WIDTH, 3), np.uint8)
        
        for i in range(0,len(img)):
            for j in range(0, len(img[0])):
                img[i][j]=(255,255,255)

        left_encoding = ''
        structure = self.__FIRST_NUM_CODES[code[0]]
        start_width = self.__HORIZONTAL_QUIET_ZONE*self.__UNIT_SIZE
        start_width = self.draw_code(img, self.__FIRST_LAST, start_width, True)

        for i in range(0, 6):
            if structure[i] == 'odd':
                left_encoding += self.__LEFT_ODD_CODES[code[i+1]]
                start_width = self.draw_code(img, self.__LEFT_ODD_CODES[code[i+1]], start_width, False)
            else:
                left_encoding += self.__LEFT_EVEN_CODES[code[i+1]]
                start_width = self.draw_code(img, self.__LEFT_EVEN_CODES[code[i+1]], start_width, False)
                
        right_encoding = ''
        start_width = self.draw_code(img, self.__MIDDLE, start_width, True)

        for x in code[7:]:
            right_encoding += self.__RIGHT_CODES[x]
            start_width = self.draw_code(img, self.__RIGHT_CODES[x], start_width, False)

        start_width = self.draw_code(img, self.__FIRST_LAST, start_width, True)

        self.add_code_to_barcode(img, code)

        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite('../EAN13.png', img)

    def draw_code(self, img, code, start_width, is_higher):
        if is_higher:
            end=self.__HORIZONTAL_QUIET_ZONE+\
                self.__BARCODE_HEIGHT+\
                self.__HEIGHT_NUM
        else:
            end=self.__HORIZONTAL_QUIET_ZONE+\
                self.__BARCODE_HEIGHT
                
        for x in code:
            if x == '1':
                cv.line(img, 
                        (start_width, self.__HORIZONTAL_QUIET_ZONE*self.__UNIT_SIZE),
                        (start_width, end*self.__UNIT_SIZE), 
                        (0,0,0), 
                        self.__UNIT_SIZE)
                        
            start_width+=self.__UNIT_SIZE

        return start_width

    def add_code_to_barcode(self, img, code):
        position = ((self.__HORIZONTAL_QUIET_ZONE)*self.__UNIT_SIZE-15,
                    (self.__VERTICAL_QUIET_ZONE+self.__BARCODE_HEIGHT+self.__HEIGHT_NUM)*self.__UNIT_SIZE)
        
        cv.putText(img,
                   code[0], 
                   position,
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.7,
                   (0,0,0),
                   2)

        position = (self.__HORIZONTAL_QUIET_ZONE*self.__UNIT_SIZE+6,
                    (self.__VERTICAL_QUIET_ZONE+self.__BARCODE_HEIGHT+self.__HEIGHT_NUM)*self.__UNIT_SIZE)

        cv.putText(img,
                   code[1:7], 
                   position,
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.7,
                   (0,0,0),
                   2)

        position = ((self.__HORIZONTAL_QUIET_ZONE+3+7*6+5)*self.__UNIT_SIZE-2,
                    (self.__VERTICAL_QUIET_ZONE+self.__BARCODE_HEIGHT+self.__HEIGHT_NUM)*self.__UNIT_SIZE)

        cv.putText(img,
                   code[7:13], 
                   position,
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.7,
                   (0,0,0),
                   2)