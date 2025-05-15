// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

package com.metrics.halstead;
/**
 * @author  Ahmed Metwally
 * source: https://github.com/aametwally/Halstead-Complexity-Measures
 */


// This class is intended to calculate all the halstead complexity metrics
public class HalsteadMetrics {

	public int DistOperators, DistOperands, TotOperators, TotOperands;
	private int Vocabulary=0;
	private int Proglen=0;
	private double CalcProgLen=0;
	private double Volume=0;
	private double Difficulty=0;
	private double Effort=0;
	private double TimeReqProg=0;
	private double TimeDelBugs=0;


	// Initialize the variables in the constructor
	public HalsteadMetrics() {
		DistOperators=0;
		DistOperands=0;
		TotOperators=0;
		TotOperands=0;
	}



	// set number of DistOperators, DistOperands, TotOperators, and TotOperands
	public void setParameters(int DistOprt, int DistOper, int TotOprt, int TotOper)
	{
		DistOperators=DistOprt;
		DistOperands=DistOper;
		TotOperators=TotOprt;
		TotOperands=TotOper;
	}



	// calculate the Program vocabulary
	public int getVocabulary()
	{
		Vocabulary=DistOperators+DistOperands;
		System.out.println("Vocabulary= "+ Vocabulary);
		return Vocabulary;
	}



	// calculate the Program length
	public int getProglen()
	{
		Proglen=TotOperators+TotOperands;
		System.out.println("Program Length= "+ Proglen);
		return Proglen;
	}



	// calculate the Calculated program length
	public double getCalcProgLen()
	{
		CalcProgLen = DistOperators*(Math.log(DistOperators) / Math.log(2)) + DistOperands*(Math.log(DistOperands) / Math.log(2));
		System.out.println("Calculated Program Length= "+ CalcProgLen);
		return CalcProgLen;
	}



	// calculate the Volume
	public double getVolume()
	{
		Volume=(TotOperators+TotOperands)*(Math.log(DistOperators+DistOperands)/Math.log(2));
		//System.out.println("Volume = "+ Volume);
		return Volume;
	}



	// calculate the Difficulty
	public double getDifficulty()
	{
		Difficulty=(DistOperators/2)*(TotOperands/(double)DistOperands);//
		System.out.println("Difficulty= "+ Difficulty);
		return Difficulty;
	}



	// calculate the Effort
	public double getEffort()
	{
		Effort=((DistOperators/2)*(TotOperands/(double)DistOperands)) * ((TotOperators+TotOperands)*(Math.log(DistOperators+DistOperands)/Math.log(2)));
		System.out.println("Effort= "+ Effort);
		return Effort;
	}



	// calculate the Time required to program
	public double getTimeReqProg()
	{
		TimeReqProg=(((DistOperators/2)*(TotOperands/(double)DistOperands)) * ((TotOperators+TotOperands)*(Math.log(DistOperators+DistOperands)/Math.log(2)))) /18;
		System.out.println("Time Required to Program= "+ TimeReqProg + " seconds");
		return TimeReqProg;
	}



	// calculate the Number of delivered bugs
	public double getTimeDelBugs()
	{
		TimeDelBugs = ((TotOperators+TotOperands)*(Math.log(DistOperators+DistOperands)/Math.log(2))) / 3000;
		System.out.println("Number of delivered bugs= "+ TimeDelBugs);
		return TimeDelBugs;
	}
}
