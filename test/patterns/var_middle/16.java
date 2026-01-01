// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.function.Function;
import java.util.Optional;

public class Test {
    private ArrayList<Long> array;

    public void setArray(ArrayList<Long> newArray) {
        array = newArray;
    }

    public ArrayList<Long> filterWithOptionalEmpty(Long threshold) {
        Function<Long, Long> filter = last -> {
            final Optional<Long> size;
            if (last >= threshold) {
                size = Optional.empty();
            } else {
                size = Optional.of(last);
            }
            return size;
        };

        return array.map(filter);
    }
}
