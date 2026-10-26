
# 设置网站的Header


class SetHeader(object):

    def set_header(self):
        headers = {
                "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjdiNjAyNGE1LTAxNzMtNGU0Zi1iZWRiLWZkOGVlMWViZDI1NSJ9.oy0KD0nuZYh9Bq2jVNdJbq9Alxhmrw94upEc-HHcuz4OHwFIrmqe1HHNun7_8tqPTRigoycX2MZaxTzTf0KH1A",
                "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjdiNjAyNGE1LTAxNzMtNGU0Zi1iZWRiLWZkOGVlMWViZDI1NSJ9.oy0KD0nuZYh9Bq2jVNdJbq9Alxhmrw94upEc-HHcuz4OHwFIrmqe1HHNun7_8tqPTRigoycX2MZaxTzTf0KH1A"
            }
        return headers


if __name__ == '__main__':
    h = SetHeader()
    headers = h.set_header()
    print(headers)