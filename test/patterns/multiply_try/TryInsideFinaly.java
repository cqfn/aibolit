// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Foo {
	public void storePerson(Person input){
		try{
		//Dangerous Operation
		} catch (AnyException ae) {
		}
		finally {
			try {
			//close connection but it may fail too
			} catch (IOException ioe) {
			//Log that
			}
		}
    }
}
