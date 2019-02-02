#/usr/bin/python3
"""
author: xiche
create at: 12/06/2018
description:
    Common utils for performance test result
Change log:
Date        Author      Version    Description
12/06/2018   xiche       1.0       Init

"""
import sys
sys.path.insert(0, r"\\nj.pfs.net\departments\Development\Team Engineering\xiche\pythonlib")
from sqlalchemy import Column, DateTime, Float, String, create_engine, Integer, ForeignKey, exists, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class TestCase(Base):
    __tablename__ = 'TestCase'
    id = Column(Integer, primary_key=True)
    TestCaseName = Column(String(50))
    Rows = Column(Integer)
    TestDetails = relationship('TestDetail')

class TestResult(Base):
    __tablename__ = 'TestResult'

    id = Column(Integer, primary_key=True)
    TestTime = Column(DateTime)
    TestVersion = Column(String(40))
    APPVersion = Column(String(100))
    Computer = Column(String(20))
    TotalTimeMinutes = Column(Float)
    CPU = Column(String(20))
    Memory = Column(String(20))
    TestDetails = relationship('TestDetail')
    
class TestDetail(Base):
    __tablename__ = 'TestDetail'

    id = Column(Integer, primary_key=True)
    CostTimeSeconds = Column(Float)
    CostTimeMinutes = Column(Float)
    TestResultID = Column(Integer, ForeignKey('TestResult.id'))
    # TestCaseName = Column(String(100))
    # MessageType = Column(String(50))
    TestCaseID = Column(Integer, ForeignKey('TestCase.id'))
        
class TestResultUtils():
    def __init__(self, db_sqlnet='xxx', db_name='xxx', db_user='xxx', db_password='xxx'):
        self.engine = create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.format(db_user, db_password, db_sqlnet, db_name))
        DBSession = sessionmaker(bind=self.engine, autoflush=False)
        self.session = DBSession()

    def save_test_result(self, test_result = None, test_case_list = [], test_detail_list = []):
        # testcase = self.session.query(TestCase).filter(TestCase.TestCaseName.like('%Coll%')).one()
        # print('type:', type(testresult))
        # print('name:', testresult.Memory)
            
        count = self.session.query(TestResult).filter(TestResult.TestTime == test_result.TestTime).count()
        if(count > 0):
            test_result = self.session.query(TestResult).filter(TestResult.TestTime == test_result.TestTime).first()

        if(len(test_case_list) != len(test_detail_list)):
            print("test case list and test detail list size is not matched.")
            return
        test_case_list_new = []
        for index, test_detail in enumerate(test_detail_list):
            test_case = test_case_list[index]
            count = self.session.query(TestCase).filter(TestCase.TestCaseName == test_case_list[index].TestCaseName and TestCase.Rows == test_case_list[index].TestCaseName.Rows).count()
            if(count > 0):
                test_case = self.session.query(TestCase).filter(TestCase.TestCaseName == test_case_list[index].TestCaseName and TestCase.Rows == test_case_list[index].TestCaseName.Rows).first()
            test_case.TestDetails.append(test_detail)
            test_result.TestDetails.append(test_detail)
            test_case_list_new.append(test_case)

        for test_case in test_case_list_new:
            self.session.add(test_case)
        self.session.add(test_result)
        
        try:
            self.session.commit()
            self.session.close()
        except exc.SQLAlchemyError as e:
            print(str(e))
        
if __name__ == '__main__':

    testResultUtils = TestResultUtils()
    
    new_testresult = TestResult(TestTime=datetime.now(), TestVersion='aaa', APPVersion='PAM800', Computer='Mort01', TotalTimeMinutes=12.2, CPU="4 Cores",Memory="16GB" )
    
    new_testcase_01 = TestCase(TestCaseName='01_Colleteral', Rows = 100)
    new_testcase_02 = TestCase(TestCaseName='04_Apprival', Rows = 300)

    new_testdetail1 = TestDetail(CostTimeMinutes = 12, CostTimeSeconds = 720)
    new_testdetail2 = TestDetail(CostTimeMinutes = 13, CostTimeSeconds = 780)

    # new_testcase.TestDetails.append(new_testdetail)
    new_testcase_list = []
    new_testcase_list.append(new_testcase_01)
    new_testcase_list.append(new_testcase_02)

    new_testdetail_list = []
    new_testdetail_list.append(new_testdetail1)
    new_testdetail_list.append(new_testdetail2)
    
    testResultUtils.save_test_result(test_result=new_testresult, test_case_list=new_testcase_list, test_detail_list=new_testdetail_list)

