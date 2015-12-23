import os
import warnings
import time
import glob


class DataForTestingMappers(object):
    def __init__(self):
        ''' Find test files and corresponsing mapper names '''
        existingTestFiles = self.find_existing_files()
        filesAndMappers = self.identify_mappers(existingTestFiles)

        self.mapperData = filesAndMappers

    def find_existing_files(self):
        ''' Find all files for testsing inside MAPPER_TEST_DATA_DIR'''
        testFiles = []

        testDataEnv = os.getenv('MAPPER_TEST_DATA_DIR')
        if testDataEnv is not None:
            testDataDirs = testDataEnv.split(':')
            for testDataDir in testDataDirs:
                if os.path.isdir(testDataDir):
                    testFiles += glob.glob(os.path.join(testDataDir, '*', '*'))

        testFiles = [testFile for testFile in testFiles if self.readable(testFile)]

        return testFiles

    def identify_mappers(self, testFiles):
        ''' From the sub-directory name get the name of the mapper '''

        mapperNames = [os.path.split(os.path.split(testFile)[0])[1] for testFile in testFiles]
        return zip(testFiles, mapperNames)


    def readable(self, testFile):
        ''' Test if file is readable at OS level '''
        if not os.path.exists(testFile):
            return False
        if not os.access(testFile, os.R_OK):
            return False
        if os.stat(testFile).st_size == 0:
            return False

        return True
