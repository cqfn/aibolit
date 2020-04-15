	public class Parser implements ParserConstants {

	  final public void ntDefinitions() throws ParseException {
		label_1:
		while (true) {
		  switch ((jj_ntk==-1)?jj_ntk():jj_ntk) {
		  case IDENTIFIER:
		  case 7:
		  case 12:
		  case 15:
		  case 16:
		  case 17:
		  case 18:
		  case 20:
		  case 38:
			;
			break;
		  default:
			jj_la1[0] = jj_gen;
			break label_1;
		  }
		  switch ((jj_ntk==-1)?jj_ntk():jj_ntk) {
		  case 38:
			ntExtendedAttributeListNonEmpty();
			break;
		  default:
			jj_la1[1] = jj_gen;
			;
		  }
		  ntDefinition();
		}
	  }
	  
	}