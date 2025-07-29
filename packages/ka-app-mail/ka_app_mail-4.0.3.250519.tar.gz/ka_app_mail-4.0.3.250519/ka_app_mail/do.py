import sys
from ka_uts_com.com import Com
from ka_app_mail.parms import Parms
from ka_app_mail.task import Task


class Do:

    @classmethod
    def do(cls) -> None:
        Task.do(Com.sh_kwargs(cls, Parms.d_eq, sys.argv))


if __name__ == "__main__":
    Do.do()
