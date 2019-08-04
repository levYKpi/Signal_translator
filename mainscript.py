import scanner as sc
import parser
import generator


def main():
    scan = sc.Scanning()
    scan.scan("signaltest")
    # scan.scan("testerrors")
    scan.print_lexemes()
    scan.print_key_words()
    scan.print_consts()
    scan.print_idents()
    scan.print_errors()
    pr = parser.Parser(scan.get_lexemes(), scan.get_key_words(),
                       scan.get_consts(), scan.get_idents(), scan.get_complex())
    pr.parsing()
    gn = generator.Generator()
    gn.compile(pr.get_tree().get_root())
    print(gn.text)
    print(gn.errors)


if __name__ == "__main__":
    main()
