// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/**
 *
 */

/**
 * @author Ahmed Metwally
 * source: https://github.com/aametwally/Halstead-Complexity-Measures
 */

package com.metrics.halstead;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import org.eclipse.jdt.core.compiler.IProblem;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.JavaCore;
import java.util.Arrays;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.util.Hashtable;
public class App {
	// construct AST of the .java files
	public static ASTVisitorMod parse(char[] str, String file) {
		ASTParser parser = ASTParser.newParser(AST.JLS13);

Hashtable<String, String> options = JavaCore.getDefaultOptions();
options.put(JavaCore.COMPILER_SOURCE, JavaCore.VERSION_13);
options.put(JavaCore.COMPILER_COMPLIANCE, JavaCore.VERSION_13);

options.put(JavaCore.COMPILER_CODEGEN_TARGET_PLATFORM, JavaCore.VERSION_13);
parser.setCompilerOptions(options);


		parser.setSource(str);
		parser.setKind(ASTParser.K_COMPILATION_UNIT);
		parser.setResolveBindings(true);
		final CompilationUnit cu = (CompilationUnit) parser.createAST(null);

		// Check for compilationUnits problems in the provided file
		IProblem[] problems = cu.getProblems();
		for(IProblem problem : problems) {
			// Ignore some error because of the different versions.
                        if (problem.getID() == 1610613332) 		 // 1610613332 = Syntax error, annotations are only available if source level is 5.0
                            continue;
                        else if (problem.getID() == 1610613329) // 1610613329 = Syntax error, parameterized types are only available if source level is 5.0
                            continue;
                        else if (problem.getID() == 1610613328) // 1610613328 = Syntax error, 'for each' statements are only available if source level is 5.0
                            continue;
                        else
                        {
                            // quit compilation if
    	                    System.out.println(file + "  CompilationUnit problem Message " + problem.getMessage() + " \t At line= "+problem.getSourceLineNumber() + "\t Problem ID="+ problem.getID());

                            //System.out.println("The program will quit now!");
                            //System.exit(1);
                        }
	        }

		// visit nodes of the constructed AST
		ASTVisitorMod visitor= new ASTVisitorMod();
		cu.accept(visitor);

	    return visitor;
	}



	// parse file in char array
	public static char[] ReadFileToCharArray(String filePath) throws IOException {
		StringBuilder fileData = new StringBuilder(1000);
		BufferedReader reader = new BufferedReader(new FileReader(filePath));
		char[] buf = new char[10];
		int numRead = 0;
		while ((numRead = reader.read(buf)) != -1) {
			String readData = String.valueOf(buf, 0, numRead);
			fileData.append(readData);
			buf = new char[1024];
		}
		reader.close();

		return  fileData.toString().toCharArray();
	}



	// parse files in a directory to list of char array
	public static List<char[]> ParseFilesInDir(List<String> JavaFiles) throws IOException{
		if(JavaFiles.isEmpty())
		{
			System.out.println("There is no java source code in the provided directory");
			System.exit(0);
		}

		List<char[]> FilesRead= new ArrayList<char []>();

		for(int i=0; i<JavaFiles.size(); i++)
		{
			//System.out.println("Now, reading: "+ JavaFiles.get(i));
			FilesRead.add(ReadFileToCharArray(JavaFiles.get(i)));
		}

		return FilesRead;
	}



	// retrieve all .java files in the directory and subdirectories.
	public static List<String> retrieveFiles(String directory) {
		List<String> Files = new ArrayList<String>();
		File dir = new File(directory);

		if (!dir.isDirectory())
		{
			 System.out.println("The provided path is not a valid directory");
			 System.exit(1);
		}

		for (File file : dir.listFiles()) {
			if(file.isDirectory())
			{
				Files.addAll(retrieveFiles(file.getAbsolutePath()));
			}
			else{
                            if (file.getName().endsWith((".java")))
			    {
				Files.add(file.getAbsolutePath());
			    }
                        }
		}

		return Files;
	}

	public static void main(String[] args) throws IOException {
		String DirName=null;
		DirName = args[0];

		// retrieve all .java files in the directory and subdirectories.
		//List<String> JavaFiles=retrieveFiles(DirName);
                List<String> JavaFiles=Arrays.asList(DirName);

		// parse files in a directory to list of char array
		List<char[]> FilesRead=ParseFilesInDir(JavaFiles);

		ASTVisitorMod ASTVisitorFile;
		int DistinctOperators=0;
		int DistinctOperands=0;
		int TotalOperators=0;
		int TotalOperands=0;
		int OperatorCount=0;
		int OperandCount=0;

		// Construct the AST of each java file. visit different nodes to get the number of operors and operands
		// Retrieve the number of distinct operators, distinct operands,
		// total operators, and total operands for each .java file in the directory.
		// Sum each parameter from different files together to be used in Halstead Complexity metrics.
		for(int i=0; i<FilesRead.size(); i++)
		{
			//System.out.println("Now, AST parsing for : "+ JavaFiles.get(i));
			ASTVisitorFile=parse(FilesRead.get(i), JavaFiles.get(i));
			DistinctOperators=ASTVisitorFile.oprt.size();
			DistinctOperands=ASTVisitorFile.names.size();

			OperatorCount=0;
			for (int f : ASTVisitorFile.oprt.values()) {
				OperatorCount+= f;
			}
			TotalOperators=OperatorCount;
			OperandCount=0;
			for (int f : ASTVisitorFile.names.values()) {
				OperandCount += f;
			}
			TotalOperands=OperandCount;

                        HalsteadMetrics hal = new HalsteadMetrics();
                        hal.setParameters(DistinctOperators, DistinctOperands, TotalOperators, TotalOperands);
                        double volume = hal.getVolume();
                        System.out.println(volume);
                        //writeUsingFiles(new String(JavaFiles.get(i)) + ";" + String.valueOf(volume));
		}
	}



public static void writeUsingFiles(String data) throws IOException
{
    BufferedWriter writer = new BufferedWriter(
                                new FileWriter("02/halstead_metric.csv", true)  //Set true for append mode
                            );
    writer.newLine();   //Add new line
    writer.write(data);
    writer.close();
}
}
