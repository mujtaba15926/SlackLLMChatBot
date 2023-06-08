import pandas as pd


def auto_truncate(val):
    return val[:1000]


home_products = pd.read_csv("home_depot_data.csv", converters={
                            'name': auto_truncate,
                            'description': auto_truncate,
                            'overview': auto_truncate})
home_products = home_products.drop(['source', 'images', 'sku_id',
                                    'total_reviews', 'crawled_at', 'currency', 'specifications', 'overview'], axis=1)
home_products['price'].replace('', None, inplace=True)
home_products['color'].replace('', None, inplace=True)
home_products['avg_rating'].replace('', None, inplace=True)
home_products.dropna(
    subset=['price', 'color', 'avg_rating', 'breadcrumbs'], inplace=True)
home_products = home_products.astype(str)
product_metadata = (home_products.to_dict(orient='index'))
