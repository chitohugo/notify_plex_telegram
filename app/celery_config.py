# from celery import Celery
# from dependency_injector.wiring import inject, Provide
#
# from containers import Container
#
#
#
# # def make_celery():
# #     celery = Celery(
# #         'tasks',
# #         broker_url='redis://redis:6379/0',
# #         broker='redis://redis:6379/0',
# #         # include = ['app.tasks']
# #     )
# #     return celery
#
# @inject
# def make_celery(app: Celery = Provide[Container.celery_service]):
#     return app
#
#
# app = make_celery()