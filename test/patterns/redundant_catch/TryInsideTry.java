// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
	public void storePerson(Person input) throws IOException {
	  try{
		validatePerson(); // if person is not valid, don't go through the flow
		try{
		  writeInLog("I will be storing this person: " + input.getName());
		}
		catch(IOException e){
		  System.out.println("Should have generated a logFile first, but hell, this won't put the flow in jeopardy.");
		}
		performPersistenceTasks(input);

	  }
	  catch(Exception e){
		e.printStackTrace();
		throw new Exception("Couldn't store the person");
	  }
    }
}
