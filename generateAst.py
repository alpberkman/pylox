import sys


class GenerateAst:
	def defineAst(outputDir, baseName, types):
		path = outputDir + "/" + baseName + ".py"
		file = open(path, "w")
		file.write("import Expr")
		file.close()
	

if __name__ == "__main__":
	if len(sys.argv) != 1:
		print("Usage: generate_ast <output directory>", file=sys.stderr)
		sys.exit(64)
		
	outputDir = sys.argv[0]
	GenerateAst.defineAst(outputDir, "Expr", [
        "Binary : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal : Object value",
        "Unary : Token operator, Expr right"])