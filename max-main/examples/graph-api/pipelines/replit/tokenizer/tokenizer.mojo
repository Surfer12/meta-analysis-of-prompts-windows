# ===----------------------------------------------------------------------=== #
# Copyright (c) 2024, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #

"""Module containing a trait for the Replit tokenizer."""

from collections import Optional, List


trait Tokenizer(Movable):
    def is_end_of_text(self, val: Int64) -> Bool:
        ...

    def encode(
        self,
        input_string: List[String],
        bos: Optional[String] = None,
        eos: Optional[String] = None,
        pad_to_multiple_of: Optional[Int] = None,
    ) -> (List[Int64], List[Int64]):
        ...

    def decode(mut self, output_tokens: List[Int64]) -> String:
        ...
