import logging

logging.getLogger("src")


def load_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        logging.warning(f"파일 '{file_path}'을(를) 찾을 수 없습니다.")
    except Exception as e:
        logging.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")


def load_talkchannel(**args):
    file_content = load_from_file('./source/project_data_카카오톡채널.txt')
    if file_content is not None:
        # logging.debug("파일 내용:", file_content)
        return file_content


def load_sink(**args):
    file_content = load_from_file('./source/project_data_카카오싱크.txt')
    if file_content is not None:
        # logging.debug("파일 내용:", file_content)
        return file_content

def load_social(**args):
    file_content = load_from_file('./source/project_data_카카오소셜.txt')
    if file_content is not None:
        # logging.debug("파일 내용:", file_content)
        return file_content
