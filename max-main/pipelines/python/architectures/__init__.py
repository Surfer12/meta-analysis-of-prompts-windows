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

from max.pipelines import PIPELINE_REGISTRY


def register_all_models():
    """Imports model architectures, thus registering the architecture in the shared PIPELINE_REGISTRY."""
    import coder as coder
    import llama3 as llama3
    import llama_vision as llama_vision
    import pixtral as pixtral
    import replit as replit
    from mistral import mistral_arch

    PIPELINE_REGISTRY.register(mistral_arch)


__all__ = ["register_all_models"]
