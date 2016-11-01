

if __name__ == '__main__':

    import os
    import sys

    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(app_dir)

    from main.app import App

    App(app_dir).main()
