import magic as m
i = m.from_file("testing", mime=True)
print(i)
if i == "application/pdf":
    print("PDF!")
else:
    print("No")