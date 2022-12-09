#!/usr/bin/env python3

import sys


class GenerateAst:
    def defineAst(outputDir, baseName, types):
        path = outputDir + "/" + baseName + ".py"
        file = open(path, "w")
        file.write("\n\nclass " + baseName + ":\n    pass\n\n")
        for type in types:
            className = type.split(":")[0][:-1]
            fields = type.split(":")[1]
            GenerateAst.defineType(file, baseName, className, fields)
        file.close()

    def defineType(file, baseName, className, fieldList):
        fields = fieldList.split(",")
        file.write("class " + className + "(" + baseName + "):\n")
        file.write("    def __init__(self, " + fieldList + " ):\n")
        for field in fields:
            file.write("        self." + field + " = " + field + "\n")
        file.write("    def accept(self, visitor):\n")
        file.write("        return visitor.visit" +
                   className + baseName + "(self)\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)
        f1()
    outputDir = sys.argv[1]
    GenerateAst.defineAst(outputDir, "Expr", [
        "Binary : left, operator, right",
        "Grouping : expression",
        "Literal : value",
        "Unary : operator, right"])
