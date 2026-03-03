\subsection{Relevance of Boundary-Specific Synthesis}

The proposed method gives special treatment to the boundary zone, using patch selection oriented along local angles to construct the interface. The importance of this specific step can be evaluated as follows:

\begin{itemize}
    \item \textbf{Experiment}: We disable the angle-aware patch selection for the boundary zone, and synthesize the boundary using the same standard non-parametric texture synthesis applied to the salt and rock interiors, without considering the local orientation of the interface.
    \item \textbf{Hypothesis}: We predict that this change would lead to less coherent and realistic boundaries. We would lose the fine-grained textural details that align with the curve of the salt dome, resulting in visible artifacts and a less convincing transition between the geological layers.
    \item \textbf{Evaluation}: A direct comparison of the boundary regions between this ablated version and the full model, both qualitatively by experts and quantitatively (if a suitable measure for boundary coherence is defined), would highlight the value of this specialized synthesis step.
\end{itemize}