from src.woori_crawler import WooriCrawler
import pandas as pd

crawler = WooriCrawler()

data = crawler.crawl()
data = pd.DataFrame(data=[], columns=['날짜','아이디','별점','리뷰','답변'])
data.to_csv('woori_bank_app_review.csv', encoding='utf-8')
