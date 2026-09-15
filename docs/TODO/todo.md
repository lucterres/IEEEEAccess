
\subsubsection{Low-data Regime Analysis}

To further characterize the augmentation benefit in the low-data regime — the primary motivating scenario of this work (offshore exploration with scarce annotated data) — both scenarios are also evaluated with limited real training sets: $N_{\text{real}} \in \{50, 100, 200\}$. The synthetic pool is adjusted proportionally (200~images for $N{=}50$ and $N{=}100$; 400~images for $N{=}200$). The fixed 800-image real test set remains unchanged.


\textcolor{red}{\textbf{[TODO: Insert IoU $\times N$ curve (Scenario~A vs.\ Scenario~B) and discussion. Expected outcome: the augmentation benefit is more pronounced under data scarcity, consistent with the core motivation of the method.]}}



% --- TABELAS DO EXPERIMENTO SEQUENCIAL (substituído pelo experimento cego) ---
% Mantidas aqui como referência histórica; serão substituídas pelos resultados do experimento cego.
\begin{comment}
\begin{table*}[htbp]
\centering
\caption{Result table: real images evaluation by the experts.}
\label{tab:real_images_evaluation}
\sisetup{output-decimal-marker = {,}}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5]@{}}
\toprule
& \multicolumn{3}{c}{\textbf{Expert 1}} & \multicolumn{3}{c}{\textbf{Expert 2}} & \multicolumn{3}{c}{\textbf{Expert 3}} & \textbf{Mean} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10}
\textbf{Measures} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{F1-score}} \\
\midrule
Std Dev & 0.06034 & 0.04584 & 0.04037 & 0.05429 & 0.04763 & 0.04408 & 0.04780 & 0.05288 & 0.03414 & 0.03953 \\
Mean & 0.91480 & 0.91563 & 0.91396 & 0.91845 & 0.90420 & 0.91064 & 0.82958 & 0.81400 & 0.82017 & 0.88159 \\
\bottomrule
\end{tabular*}
\end{table*}

\begin{table*}[htbp]
\centering
\caption{Result table: Synthetic images evaluation by the experts.}
\label{tab:synthetic_images_evaluation}
\sisetup{output-decimal-marker = {,}}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5] S[table-format=1.5]@{}}
\toprule
& \multicolumn{3}{c}{\textbf{Expert 1}} & \multicolumn{3}{c}{\textbf{Expert 2}} & \multicolumn{3}{c}{\textbf{Expert 3}} & \textbf{Mean} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10}
\textbf{Measures} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{Precision}} & {\textbf{Recall}} & {\textbf{F1-score}} & {\textbf{F1-score}} \\
\midrule
Std Dev & 0.06706 & 0.04698 & 0.04509 & 0.05597 & 0.05397 & 0.04433 & 0.05221 & 0.05644 & 0.03889 & 0.04277 \\
Mean & 0.90439 & 0.89575 & 0.89868 & 0.88823 & 0.87772 & 0.88186 & 0.83354 & 0.82261 & 0.82648 & 0.86901 \\
\bottomrule
\end{tabular*}
\end{comment}