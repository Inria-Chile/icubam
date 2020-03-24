from absl import logging
import os.path
import tornado.ioloop
from tornado import queues
import tornado.web

from icubam import config
from icubam.db import queue_writer
from icubam.db import sqlite
from icubam.www import token
from icubam.www.handlers import home
from icubam.www.handlers import update


class WWWServer:
  """Serves and manipulates the ICUBAM data."""

  def __init__(self, db_path, port):
    self.port = port
    self.routes = []
    self.writing_queue = queues.Queue()
    self.db = sqlite.SQLiteDB(db_path)
    self.make_app()
    self.callbacks = [
      queue_writer.QueueWriter(self.writing_queue, self.db)
    ]

  def add_handler(self, handler, **kwargs):
    route = os.path.join('/', handler.ROUTE)
    self.routes.append((route, handler, kwargs))
    logging.info('{} serving on {}'.format(handler.__name__, route))

  def make_app(self):
    self.add_handler(update.UpdateHandler, queue=self.writing_queue)
    self.add_handler(home.HomeHandler, db=self.db)
    self.routes.append(
      (r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {"path": "icubam/www/static/"})
    )

  @property
  def debug_str(self):
    """Only for debug to be able to connect for now. To be removed."""
    return 'Connect to http://localhost:{}{}?id={}'.format(
      self.port, update.UpdateHandler.ROUTE, token.encode_icu(1, 'A. Beclere'))

  def run(self):
    logging.info('Running {} on port {}'.format(
      self.__class__.__name__, self.port))
    logging.info(self.debug_str)

    settings = {
      "cookie_secret": config.SECRET_COOKIE,
      "login_url": "/error",
    }
    app = tornado.web.Application(self.routes, **settings)
    app.listen(self.port)

    io_loop = tornado.ioloop.IOLoop.current()
    for callback_obj in self.callbacks:
      io_loop.spawn_callback(callback_obj.process)

    io_loop.start()