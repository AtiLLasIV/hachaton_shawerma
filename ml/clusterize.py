#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import json
import joblib

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score


def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Преобразует список строк в эмбеддинги через sentence-transformers.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(
        texts, show_progress_bar=True, convert_to_numpy=True
    )
    return embeddings


def choose_pca_dim(embeddings: np.ndarray, variance_threshold: float) -> PCA:
    """
    Выбирает число компонент PCA до достижения порога кумулятивной дисперсии.
    """
    pca_full = PCA().fit(embeddings)
    cumvar = np.cumsum(np.nan_to_num(pca_full.explained_variance_ratio_, nan=0.0))
    d = np.searchsorted(cumvar, variance_threshold) + 1
    d = min(d, embeddings.shape[1])
    print(f"Выбрано компонент PCA: {d} (кумулятивная дисперсия {cumvar[d-1]:.3f})")
    return PCA(n_components=d)


def find_best_k(
    emb: np.ndarray,
    k_min: int,
    k_max: int,
    n_samples: int = 10,
    batch_size: int = 10000,
    random_state: int = 42
) -> MiniBatchKMeans:
    """
    Подбирает K, равномерно выбрав до n_samples значений между k_min и k_max,
    и выбирает то, при котором silhouette_score максимален, используя MiniBatchKMeans.
    """
    n = emb.shape[0]
    k_max = min(k_max, n - 1)
    ks = np.linspace(k_min, k_max, num=min(n_samples, max(0, k_max - k_min + 1)), dtype=int)
    ks = sorted(set(ks))

    best_score = -1.0
    best_model = None
    print(f"Тестируем K: {ks}")
    for k in ks:
        if k < 2:
            continue
        mbk = MiniBatchKMeans(
            n_clusters=k,
            batch_size=batch_size,
            random_state=random_state
        )
        labels = mbk.fit_predict(emb)
        score = silhouette_score(emb, labels)
        print(f"K={k}: silhouette_score={score:.4f}")
        if score > best_score:
            best_score = score
            best_model = mbk
    if best_model is None:
        raise RuntimeError(f"Нет валидных K в выборке {ks}")
    print(f"Выбранное K={best_model.n_clusters} с silhouette_score={best_score:.4f}")
    return best_model


def main():
    parser = argparse.ArgumentParser(description='Кластеризация вакансий с подбором K (MiniBatch)')
    parser.add_argument('input_file', help='Файл с названиями вакансий')
    parser.add_argument('output_file', help='Куда сохранять JSON кластеров')
    parser.add_argument('--pca-file', default="pca.joblib",
                        help='Путь для сохранения состояния PCA (joblib)')
    parser.add_argument('--variance', type=float, default=0.95,
                        help='Порог cumulative explained variance для PCA')
    parser.add_argument('--kmin', type=int, default=2, help='Минимум кластеров K')
    parser.add_argument('--kmax', type=int, default=50, help='Максимум кластеров K')
    parser.add_argument('--k-samples', type=int, default=10,
                        help='Сколько вариантов K протестировать равномерно')
    parser.add_argument('--batch-size', type=int, default=10000,
                        help='Размер батча для MiniBatchKMeans')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        if not texts:
            raise ValueError("Нет непустых строк.")
    except Exception as e:
        print(f"Ошибка чтения {args.input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Эмбеддинги и PCA
    emb = embed_texts(texts)
    pca = choose_pca_dim(emb, args.variance)
    emb_reduced = pca.fit_transform(emb)
    joblib.dump(pca, args.pca_file)
    print(f"PCA model saved to {args.pca_file}")

    # Подбор K и кластеризация
    mbk_model = find_best_k(
        emb_reduced,
        args.kmin,
        args.kmax,
        n_samples=args.k_samples,
        batch_size=args.batch_size
    )

    # Формируем JSON-список кластеров с natural-language именами
    clusters = []
    labels = mbk_model.labels_
    centers = mbk_model.cluster_centers_
    for idx, center in enumerate(centers):
        # находим индекс ближайшего текста к центроиду
        cluster_idxs = np.where(labels == idx)[0]
        dists = np.linalg.norm(emb_reduced[cluster_idxs] - center, axis=1)
        rep_idx = cluster_idxs[np.argmin(dists)]
        clusters.append({
            "cluster_name": texts[rep_idx],
            "cluster_emb": center.tolist()
        })

    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(clusters, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка записи {args.output_file}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Готово! Кластеры сохранены в JSON: {args.output_file}")

if __name__ == '__main__':
    main()
