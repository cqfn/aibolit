// Copyright (c) 2019-2025 CQFN.org
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the 'Software'), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

/*******************************************************************************
 * Copyright (c) 2015-2025 Skymind, Inc.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 ******************************************************************************/

package org.nd4j.linalg.api.ops.impl.transforms.pairwise.arithmetic;

import lombok.NonNull;
import org.nd4j.autodiff.samediff.SDVariable;
import org.nd4j.autodiff.samediff.SameDiff;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.api.ops.impl.transforms.BaseDynamicTransformOp;
import org.nd4j.linalg.api.ops.impl.transforms.pairwise.arithmetic.bp.AddBpOp;

import java.util.List;

/**
 * Addition operation
 *
 * @author Adam Gibson
 */
public class AddOp extends BaseDynamicTransformOp {
    public static final String OP_NAME = "add";

    public AddOp() {
    }

    public AddOp(@NonNull SameDiff sameDiff, @NonNull SDVariable x, @NonNull SDVariable y) {
        super(sameDiff, new SDVariable[]{x, y}, false);
    }

    public AddOp(INDArray first, INDArray second, INDArray result){
        this(new INDArray[]{first, second}, result == null ? null : new INDArray[]{result});
    }

    public AddOp(@NonNull INDArray x, @NonNull INDArray y) {
        this(new INDArray[]{x,y}, null);
    }

    public AddOp(INDArray[] inputs, INDArray[] outputs) {
        super(inputs, outputs);
    }

    @Override
    public String opName() {
        return OP_NAME;
    }

    @Override
    public String onnxName() {
        return "Add";
    }

    @Override
    public String[] tensorflowNames() {
        return new String[]{"Add", "AddV2"};
    }

    @Override
    public List<SDVariable> doDiff(List<SDVariable> i_v) {
        return new AddBpOp(sameDiff, larg(), rarg(), i_v.get(0)).outputs();
    }


}
