from src.google_store_app_review_crawler import GoogleStoreAppReviewCrawler
from pandas import DataFrame

crawler = GoogleStoreAppReviewCrawler()

data = crawler.crawl(
    store_url="https://play.google.com/store/apps/details?id=com.wooribank.smart.npib&showAllReviews=true"
)

dataFrame = DataFrame(data)
dataFrame.columns=['date', 'user-name', 'star-rating', 'review', 'comment']

dataFrame.to_csv('hana_bank_app_review_data.csv', index=False)