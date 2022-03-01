import configparser
import os


class EnvVariables:

    @staticmethod
    def get_section_values(sections):
        valid_path = "demo.properties"
        cf = configparser.SafeConfigParser()
        cf.read(valid_path)

        env_variables = {}
        for section in sections:
            for key in cf.options(section):
                val = cf.get(section, key, vars=os.environ)  # use it here
                # print('### [{}] -> {}: {!r}'.format(section, key, val))
                env_variables[key.upper()] = val

        return env_variables


class Headers:
    content_headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }
    content_headers_google = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }


class Endpoint:
    sections = ["APIS"]
    env_variables = EnvVariables.get_section_values(sections)
    google_api = env_variables.get("GOOGLE_API")
