from Config import Config
from Model import Model
from OutputGenerator import OutputGenerator
import misc


def main(
    configuration_file="default_config.xlsx",
):
    misc.greet()
    config = Config(configuration_file)
    model = Model(config)
    misc.say_system_built()
    model.solve()
    misc.say_system_solved()
    output_generator = OutputGenerator(model, config)
    output_generator.generate_outputs()
    misc.say_good_bye()


if __name__ == "__main__":
    main()
