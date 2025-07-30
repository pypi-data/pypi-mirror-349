"""
本模块用于更新mysql服务器中的数据
"""
import datetime
import pandas as pd
from yangke.common.config import logger
from yangke.base import execute_function_every_day
from yangke.stock.dataset.mairuiData import StockData
from yangke.stock.dataset.storage import Storage
import yangke.stock.dataset.baostockData as bsd


class UpdateDataBase:
    def __init__(self, kind='dataset', ip=None, port=None, user=None, passwd=None, db=None):
        """
        更新股票数据至数据库
        :param kind: 可取值mysql，表示存储到mysql数据库，sqlite表示sqlite数据库，其他字符串表示存储到运行路径下的文件夹
        """
        self.已退市股票 = ['000003', '000005', '000013', '000015',
                           '000018', '000023', '000024', '000033', '000038', '000040',
                           '000046', '000047', '000150', '000151', '000405', '000406',
                           '000412', '000413', '000416', '000418', '000502', '000508',
                           '000511', '000515', '000522', '000527', '000535', '000540',
                           '000542', '000549', '000556', '000562', '000569', '000578',
                           '000583', '000584', '000585', '000587', '000588', '000594',
                           '000602', '000606', '000611', '000613', '000616', '000618',
                           '000621', '000622', '000627', '000653', '000658', '000660',
                           '000662', '000666', '000667', '000671', '000673', '000675',
                           '000687', '000689', '000693', '000699', '000730', '000732',
                           '000748', '000760', '000763', '000765', '000769', '000780',
                           '000787', '000805', '000806', '000817', '000827', '000832',
                           '000835', '000836', '000861', '000866', '000878', '000916',
                           '000918', '000939', '000956', '000961', '000971', '000976',
                           '000979', '000982', '000996', '001390', '002002', '002013',
                           '002018', '002070', '002071', '002087', '002089', '002092',
                           '002113', '002118', '002143', '002147', '002220', '002259',
                           '002260', '002280', '002288', '002308', '002325', '002336',
                           '002341', '002359', '002411', '002417', '002433', '002435',
                           '002447', '002450', '002464', '002473', '002477', '002499',
                           '002502', '002503', '002504', '002505', '002509', '002604',
                           '002610', '002618', '002619', '002621', '002665', '002680',
                           '002684', '002699', '002708', '002711', '002740', '002750',
                           '002751', '002770', '002776', '002781', '300023', '300028',
                           '300038', '300064', '300089', '300090', '300104', '300108',
                           '300116', '300117', '300156', '300178', '300186', '300202',
                           '300208', '300216', '300225', '300262', '300273', '300280',
                           '300282', '300297', '300309', '300312', '300325', '300330',
                           '300336', '300356', '300362', '300367', '300372', '300392',
                           '300431', '300495', '300506', '300526', '300742', '300799',
                           '301112', '301316', '301590', '600001', '600002', '600003',
                           '600005', '600065', '600068', '600069', '600070', '600074',
                           '600077', '600083', '600086', '600087', '600090', '600091',
                           '600092', '600093', '600102', '600112', '600122', '600139',
                           '600145', '600146', '600175', '600181', '600205', '600209',
                           '600213', '600220', '600225', '600234', '600240', '600242',
                           '600247', '600253', '600260', '600263', '600270', '600275',
                           '600277', '600286', '600290', '600291', '600296', '600297',
                           '600306', '600311', '600317', '600321', '600357', '600358',
                           '600385', '600387', '600393', '600401', '600432', '600462',
                           '600466', '600472', '600485', '600532', '600553', '600555',
                           '600565', '600591', '600607', '600614', '600625', '600627',
                           '600631', '600632', '600634', '600646', '600647', '600652',
                           '600656', '600659', '600669', '600670', '600671', '600672',
                           '600677', '600680', '600687', '600695', '600700', '600701',
                           '600705', '600709', '600723', '600747', '600752', '600762',
                           '600766', '600767', '600772', '600777', '600781', '600786',
                           '600788', '600799', '600804', '600806', '600811', '600813',
                           '600823', '600832', '600836', '600837', '600840', '600842',
                           '600849', '600852', '600856', '600870', '600878', '600890',
                           '600891', '600896', '600898', '600899', '600978', '600991',
                           '601028', '601258', '601268', '601299', '601558', '603003',
                           '603049', '603133', '603157', '603363', '603555', '603603',
                           '603963', '603996', '688086', '688555', '832317', '833874',
                           '833994']
        self.storage = Storage(kind, user, passwd, ip, port, db)
        # 新增：检查存储初始化是否成功
        if self.storage.engine is None:
            logger.error(f"存储初始化失败：{self.storage.error}")
            # 可根据需求选择退出程序或执行其他降级操作
            raise RuntimeError("存储初始化失败，请检查数据库权限或配置")
        self.ds: StockData = StockData()
        # 一次性获取所有股票当天的数据，一天多次获取可能返回None，是服务器限制了请求次数
        res = self.ds.get_daily_all()
        self.storage.update_daily_all(res)

    def update_all_holidays(self):
        """
        更新服务器上的假日信息数据，手动运行，一次更新10年的假日信息最好
        """
        holiday = bsd.get_holiday(start_date=datetime.date(
            1990, 12, 19), end_date=datetime.date(2000, 1, 1))
        self.storage.update_holiday_table(holiday)

    def update(self):
        """
        更新一次股票数据
        每次执行时，会自动检测当天所属的年份的假日数据是否存在，不存在增更新当年的假日数据

        """
        # ----------------------------- 首先更新假期表 -----------------------------------------
        # 只有tushare和baostock有假期数据
        if self.storage.need_update_holiday_table():
            holiday = bsd.get_holiday()  # 获取今年的holiday数据
            self.storage.update_holiday_table(holiday)

        # ----------------------------- 更新全部股票列表数据 ------------------------------------
        all_stocks: pd.DataFrame | None = None
        if self.storage.need_update_all_stocks_table():  # 从网络获取
            all_stocks = self.ds.get_all_stock_basic_info()
            self.storage.update_all_stocks_table(all_stocks)
        if all_stocks is None:  # 获取失败，从自建数据库获取
            all_stocks = self.storage.get_all_stock_basic_info()  # 从数据库存储中读取所有的股票信息

        last_day_desired = self.storage.get_previous_working_day(
            include_time=True)
        pre_day = self.storage.get_working_day_before_day(last_day_desired)
        daily_all = self.storage.get_daily_all_df()
        if len(daily_all) > 1 and pd.to_datetime(daily_all['trade_date'][0]).date() == last_day_desired:
            pass  # 如果daily_all中已经缓存了最新一天的数据，则不尽兴任何操作
        else:
            d1 = self.ds.get_daily_all()  # 一次性获取所有股票当天的数据
            self.storage.update_daily_all(d1)

        for index, row in all_stocks.iterrows():
            symbol = row['symbol']
            if str(symbol) in self.已退市股票:
                continue
            logger.info(f"开始更新{symbol}的日线数据，进度{index}/{all_stocks.shape[0]}")
            try:
                self.storage.create_stock_table_day(symbol)
                if self.storage.need_update_daily(symbol):  # 首先判断是否需要更新数据
                    # 其次判断表中最后一条数据的日期，如果只是缺少一条数据，只需要获取最后一天的数据即可
                    last_date = self.storage.get_last_date_of_daily_table(symbol)  # 数据库中已有的最后一天的数据
                    if last_date is None:
                        daily_data = self.ds.get_daily(symbol, end_date=last_day_desired)
                    elif last_date == pre_day:
                        d = daily_all[daily_all['symbol'] == symbol] # 拿到当日所有股票信息中symbol这一行
                        if len(d) == 1 and pd.to_datetime(d["trade_date"]).iloc[0].date() == last_day_desired:
                            daily_data = d
                        else:
                            daily_data = self.ds.get_daily_range(symbol,
                                                                 start_date=last_date + datetime.timedelta(days=1),
                                                                 end_date=last_day_desired)
                    else:
                        daily_data = self.ds.get_daily_range(symbol,
                                                             start_date=last_date + datetime.timedelta(days=1),
                                                             end_date=last_day_desired)

                    if daily_data is not None:
                        self.storage.update_daily(symbol, daily_data)
            except TimeoutError:
                logger.debug(f"获取{symbol}的日线数据失败，跳过")
        logger.debug("数据更新完成!")

    def start(self, daemon=True, test_service=False):
        if not test_service:
            execute_function_every_day(
                self.update, hour=16, minute=0, daemon=False)
        self.storage.start_rest_service(daemon=daemon)


if __name__ == "__main__":
    udb = UpdateDataBase(kind='mysql')
    udb.update()
    udb.start(test_service=True)
