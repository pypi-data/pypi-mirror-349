import pytest
from pathlib import Path
from json import loads
from jsurl import URL


class ValidCase:

  def __init__(self, params: dict):
    self.url: str = params['url']
    self.description: str = params['description']
    self.protocol: str = params['expected']['protocol']
    self.hostname: str = params['expected']['hostname']
    self.host: str = params['expected']['host']
    self.port: str = params['expected']['port']
    self.pathname: str = params['expected']['pathname']
    self.search: str = params['expected']['search']
    self.hash: str = params['expected']['hash']
    self.username: str = params['expected']['username']
    self.password: str = params['expected']['password']
    self.origin: str = params['expected']['origin']
    self.href: str = params['expected']['href']


class InvalidCase:

  def __init__(self, params: dict):
    self.url: str = params['url']
    self.description: str = params['description']


def load_cases():
  file = Path(__file__).parent / 'cases.json'

  data: dict = loads(file.read_text())

  valid = data['validURLs']
  invalid = data['invalidURLs']

  valid_cases = [ValidCase(params) for params in valid]
  invalid_cases = [InvalidCase(params) for params in invalid]

  return valid_cases + invalid_cases


@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case.description)
def test_urls(case: ValidCase | InvalidCase):

  if isinstance(case, ValidCase):
    url = URL(case.url)

    assert url.protocol == case.protocol
    assert url.hostname == case.hostname
    assert url.host == case.host
    assert url.port == case.port
    assert url.pathname == case.pathname
    assert url.search == case.search
    assert url.hash == case.hash
    assert url.username == case.username
    assert url.password == case.password
    assert url.origin == case.origin
    assert url.href == case.href

  else:
    with pytest.raises(Exception):
      URL(case.url)
