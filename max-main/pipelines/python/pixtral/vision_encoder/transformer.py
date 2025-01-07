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


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from max.dtype import DType
from max.graph import TensorValue, TensorValueLike, ops
from nn.layer import Layer

if TYPE_CHECKING:
    from nn.linear import Linear
    from nn.norm import RMSNorm

    from .attention import Attention


@dataclass
class MLP(Layer):
    """
    Simple multi-layer perceptron composed of three linear layers.
    Uses Gelu activation function.
    """

    gate_proj: Linear
    down_proj: Linear
    up_proj: Linear

    def __call__(self, x: TensorValueLike) -> TensorValue:
        return self.down_proj((ops.gelu(self.gate_proj(x)) * self.up_proj(x)))  # type: ignore


@dataclass
class TransformerBlock(Layer):
    """Stack of Attention, FeedForward, and RMSNorm layers."""

    attention: Attention
    mlp: MLP
    attention_norm: RMSNorm
    mlp_norm: RMSNorm

    def __call__(
        self,
        x: TensorValue,
        attention_mask: TensorValueLike,
        position_embeddings: TensorValue,
    ) -> tuple[TensorValue]:
        attention_out = self.attention(
            self.attention_norm(x),
            attention_mask,
            position_embeddings,  # type: ignore
        )

        h = x + attention_out
        h = h + self.mlp(self.mlp_norm(h))

        return h  # type: ignore


@dataclass
class Transformer(Layer):
    """Transformer model consisting of TransformerBlock layers.
    The input is embeddings created using convolution followed by normalization.

    The differences between this transformer and other decoder model transformers:
    1. Input to the transformer is patch embeddings created by convolutions not tokens.
    2. No linear(norm(output)) at the transformer output.
    3. It uses the 2d rotary embeddings defined for images which is different
    from the rotary embeddings defined in other classes as rope: RotaryEmbedding
    """

    n_heads: int
    layers: list[TransformerBlock]

    def __call__(
        self,
        patch_embeds,
        attention_mask,
        position_embeddings,
        **kwargs,
    ):
        h = patch_embeds

        for _, layer in enumerate(self.layers):
            h = layer(
                h,
                attention_mask,
                position_embeddings,
                **kwargs,
            )

        # Always return float32 logits, no matter the activation type
        return ops.cast(h, DType.float32)