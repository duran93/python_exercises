"""Program for obtaining a reverse complement from a sequence"""


def dna_seq_rev_comp():
    "Return the reverse complement of a sequence"
    seq_comp = dna_seq_comp()
    seq_rev_comp = ""
    for nucleotide in seq_comp:
        seq_rev_comp = str(nucleotide) + seq_rev_comp
    print(f"""
          The reverse complement sequence is:
          {seq_rev_comp}
        """)


def dna_seq_comp():
    """Return the complementary sequence"""
    user_seq = list(dna_seq())
    nucl_change = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }
    comp_seq = []
    for nucleotide in user_seq:
        comp_seq.append(nucl_change[nucleotide])
    print(f"""
          The complementary sequence is:
          {"".join(comp_seq)} 
        """)
    return comp_seq


def dna_seq():
    """Call the user for a DNA sequence and corrects it"""
    user_seq = input("DNA sequence: ").upper().strip()
    nucleotides = ["A", "G", "C", "T"]
    corr_user_seq = ""
    for nucleotide in user_seq:
        if nucleotide in nucleotides:
            corr_user_seq = corr_user_seq + nucleotide
    nucleotide_count = {"A": corr_user_seq.count("A"),
                        "G": corr_user_seq.count("G"),
                        "C": corr_user_seq.count("C"),
                        "T": corr_user_seq.count("T")
                        }
    try:
        gc_perc = ((user_seq.count("G") + user_seq.count("C")) /
                   len(user_seq))*100
        print(f"""
            The nucleotide sequence has the following composition: 
                        {nucleotide_count}
               The sequence is {len(corr_user_seq)}bp long with a {round(gc_perc,2)}% GC content.
            """)
        return corr_user_seq
    except ZeroDivisionError:
        return dna_seq()


print("""
      Welcome to the DNA sequence manipulator
      """)
while True:
    option = input("""
          Choose an option for your DNA sequence
          0 -> Obtain the complementary sequence.
          1 -> Obtain the reverse complement sequence.
          """)
    if option == "0":
        dna_seq_comp()
        option = input(
            "Do you need more sequence transformations?(Y/N): ").upper()
        while option != 0:
            if option == "N":
                exit()
            elif option == "Y":
                option = 0
            else:
                option = input(
                    "Wrong value. Do you need more sequence transformations?(Y/N): ").upper()

    elif option == "1":
        dna_seq_rev_comp()
        option = input(
            "Do you need more sequence transformations?(Y/N): ").upper()
        while option != 0:
            if option == "N":
                exit()
            elif option == "Y":
                option = 0
            else:
                option = input(
                    "Wrong value. Do you need more sequence transformations?(Y/N): ").upper()
    else:
        print("Invalid Option")
