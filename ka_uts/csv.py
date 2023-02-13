# coding=utf-8

import csv


class Csv:

    class AoA:

        @staticmethod
        def write(aoa, path_, keys_, **kwargs):
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = csv.writer(
                           fd,
                           quotechar=quote,
                           quoting=csv.QUOTE_NONNUMERIC,
                           delimiter=delimiter)
                writer.writerow(keys_)
                for arr in aoa:
                    writer.writerow(arr)

    class AoD:

        @staticmethod
        def write(aod, path_, fieldnames, **kwargs):
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = csv.DictWriter(
                    fd,
                    fieldnames=fieldnames,
                    quotechar=quote,
                    quoting=csv.QUOTE_NONNUMERIC,
                    delimiter=delimiter
                )
                writer.writeheader()
                writer.writerows(aod)

    class Dic:

        @staticmethod
        def write(dic, path_, keys_, **kwargs):
            delimiter = kwargs.get('delimiter', ',')
            quote = kwargs.get('quote', '"')
            with open(path_, 'w') as fd:
                writer = csv.writer(
                           fd,
                           quotechar=quote,
                           quoting=csv.QUOTE_NONNUMERIC,
                           delimiter=delimiter)
                writer.writerow(keys_)
                writer.writerow(dic.values())

    # class D3:
    #
    #   @staticmethod
    #   def write(d3, cfg_io_out, d3_nm, **kwargs):
    #       _sw = kwargs.get('sw_' + d3_nm)
    #       if not _sw:
    #           return
    #       today = date.today().strftime("%Y%m%d")
    #       _path = kwargs.get(f'path_out_{d3_nm}').format(today=today)
    #       # _path = cfg_io_out[d3_nm]["csv"]["path"]
    #       _keys = cfg_io_out[d3_nm]["keys"]
    #       _aoa = D3V.yield_values(d3)
    #       Csv.AoA.write(_aoa, _path, _keys, **kwargs)

    @staticmethod
    def read_to_aod(path, **kwargs):
        # def read_2dod(path, **kwargs):
        mode = kwargs.get('mode', 'r')
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path, mode) as fd:
            return csv.DictReader(fd, delimiter=delimiter, quotechar=quote)

    @staticmethod
    def read_2arr(path, **kwargs):
        mode = kwargs.get('mode', 'r')
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path, mode) as fd:
            aoa = csv.reader(fd, delimiter=delimiter, quotechar=quote)
        return aoa

    @staticmethod
    def write_aod(aod, path_, **kwargs):
        fieldnames = aod[0].keys()
        delimiter = kwargs.get('delimiter', ',')
        quote = kwargs.get('quote', '"')
        with open(path_, 'w') as fd:
            writer = csv.DictWriter(
                fd,
                fieldnames=fieldnames,
                quotechar=quote,
                quoting=csv.QUOTE_NONNUMERIC,
                delimiter=delimiter
            )
            writer.writeheader()
            writer.writerows(aod)
