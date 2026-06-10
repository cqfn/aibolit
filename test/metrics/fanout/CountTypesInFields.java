// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total FanOut = 3

public class FirstClass {
  Set set = new HashSet();      // Set is excluded from considering
  Map map = new HashMap();      // Map is excluded from considering
  Date date = new Date();       // +1 for Date
  Time time = new Time();       // +1 for Time
  Place place = new Place();    // +1 for Place
}
