from absl import app
from absl import flags
from icubam import config
from icubam.messaging import sms_sender

flags.DEFINE_string('config', 'resources/config.toml', 'Config file.')
flags.DEFINE_string('dotenv_path', None, 'Optionally specifies the .env path.')
flags.DEFINE_enum('mode', 'dev', ['prod', 'dev'], 'Run mode.')
FLAGS = flags.FLAGS


def main(argv):
  cfg = config.Config(FLAGS.config, mode=FLAGS.mode, env_path=FLAGS.dotenv_path)
  ms = sms_sender.get(cfg, sms_carrier='TW')
  ms.send("33698158092", "Test from  TW")
  ms = sms_sender.get(cfg, sms_carrier='NX')
  ms.send("33698158092", "Test from NX")
  ms = sms_sender.get(cfg, sms_carrier='MB')
  ms.send("33698158092", "Test from MB")

if __name__ == "__main__":
  app.run(main)
