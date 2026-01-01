// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
	public void storePerson(Person input) throws IOException {
		try{
		//Dangerous Operation
		} catch (AnyException ae) {
			throw ae;
		}
		finally {
			try {
			//close connection but it may fail too
			} catch (IOException ioe) {
				throw ioe;
			}
		}
    }
}
