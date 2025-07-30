import { useState, useCallback, useRef } from 'react';
import type { SavedSearch } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useSavedSearches = (sessionId: string) => {
  console.debug('[useSavedSearches] hook called, sessionId:', sessionId);
  const [searches, setSearches] = useState<SavedSearch[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestSeq = useRef(0);

  // 直接追蹤當前的搜索列表，避免閉包問題
  const searchesRef = useRef<SavedSearch[]>([]);

  // 當 searches 發生變化時，更新 searchesRef
  const updateSearchesRef = (newSearches: SavedSearch[]) => {
    searchesRef.current = newSearches;
    setSearches(newSearches);
    console.debug('[updateSearchesRef] 更新引用，新搜索列表長度:', newSearches.length);
  };

  // 提取排序邏輯為單獨的函數
  const sortSearches = useCallback((searches: SavedSearch[]) => {
    const sorted = [...searches].sort((a, b) => {
      if (a.account === "系統" && b.account !== "系統") return -1;
      if (a.account !== "系統" && b.account === "系統") return 1;
      return a.order - b.order;
    });
    console.debug('[sortSearches] sorted:', sorted);
    return sorted;
  }, []);

  // fetchSavedSearches 改為普通 async function
  async function fetchSavedSearches(force = false) {
    // 防止重複請求或無效的 sessionId
    if (isLoading && !force || !sessionId) {
      console.debug('[fetchSavedSearches] 跳過請求: isLoading=', isLoading, 'force=', force, 'sessionId存在=', !!sessionId);
      return;
    }

    const seq = ++requestSeq.current;
    try {
      console.debug('[fetchSavedSearches] 開始請求，序號:', seq);
      setIsLoading(true);
      setError(null);
      console.debug('[fetchSavedSearches] Fetching searches...');
      const response = await fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}`);

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      let arr: SavedSearch[] = Array.isArray(data) ? data : (Array.isArray(data.searches) ? data.searches : []);
      console.debug('[fetchSavedSearches] 獲取到搜索列表:', arr, '當前序號:', seq, '最新序號:', requestSeq.current);

      // 只處理最新的請求
      if (seq === requestSeq.current) {
        const sortedArr = sortSearches(arr);
        console.debug('[fetchSavedSearches] 更新搜索列表，原數量:', searchesRef.current.length, '新數量:', sortedArr.length);
        // 使用新函數更新狀態
        updateSearchesRef(sortedArr);
      } else {
        console.debug('[fetchSavedSearches] 序號不匹配，忽略結果');
      }
    } catch (error) {
      console.error('[fetchSavedSearches] Error:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch saved searches');
    } finally {
      setIsLoading(false);
    }
  }

  // 改進的 saveSearch 函數，直接返回新的搜索數據
  const saveSearch = useCallback(async (search: Omit<SavedSearch, 'id' | 'createdAt'>): Promise<SavedSearch | null> => {
    console.debug('[saveSearch] 開始保存搜索:', search, '當前isLoading=', isLoading);
    if (isLoading) {
      console.debug('[saveSearch] 已有請求在進行中，跳過');
      return null;
    }

    if (!sessionId) {
      console.debug('[saveSearch] sessionId不存在，跳過');
      return null;
    }

    setIsLoading(true);
    setError(null);
    try {
      // 發送POST請求
      console.debug('[saveSearch] 發送POST請求，數據:', search);
      const response = await fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(search),
      });

      if (!response.ok) {
        console.error('[saveSearch] POST請求失敗，狀態碼:', response.status);
        throw new Error(`Failed to save search: ${response.status}`);
      }

      // 從 POST 回應中獲取數據
      const responseData = await response.json();
      console.debug('[saveSearch] POST回應數據:', responseData);

      let newSearch: SavedSearch | null = null;

      // 直接使用回應數據更新UI
      if (responseData && typeof responseData === 'object' && responseData.id) {
        // 回應是單個搜索對象
        newSearch = responseData as SavedSearch;
        console.debug('[saveSearch] 從回應中獲取到新搜索:', newSearch);

        // 獲取當前完整的搜索列表，以避免丟失數據
        // 先獲取最新的後台數據，然後添加新搜索
        console.debug('[saveSearch] 強制獲取最新數據');
        await fetchSavedSearches(true);

        // 等待一下，確保 fetchSavedSearches 執行完成
        await new Promise(resolve => setTimeout(resolve, 100));

        // 此時 searchesRef.current 應該包含最新數據
        console.debug('[saveSearch] 系統清單更新後, 當前搜索數量:', searchesRef.current.length);

        // 將新搜索添加到列表或更新現有搜索
        const currentSearches = [...searchesRef.current];

        // 檢查是否已存在這個ID
        const exists = currentSearches.some(s => s.id === newSearch?.id);
        let updatedSearches: SavedSearch[];

        if (exists) {
          console.debug('[saveSearch] 搜索ID已存在，更新現有項');
          updatedSearches = sortSearches(
            currentSearches.map(s => s.id === newSearch?.id ? newSearch : s)
          );
        } else {
          console.debug('[saveSearch] 添加新搜索到列表', newSearch);
          updatedSearches = sortSearches([...currentSearches, newSearch]);
        }

        console.debug('[saveSearch] 最終搜索數量 - 更新前:', currentSearches.length, '更新後:', updatedSearches.length);

        // 使用新函數更新狀態
        updateSearchesRef(updatedSearches);

        // 強制立即刷新
        console.debug('[saveSearch] 保存後立即刷新一次');
        setTimeout(() => {
          fetchSavedSearches(true);
        }, 50);
      } else {
        // 回應不是預期的格式，直接獲取最新數據
        console.debug('[saveSearch] 回應格式不符合預期，獲取最新數據');
        await fetchSavedSearches(true);
      }

      return newSearch;
    } catch (error) {
      console.error('[saveSearch] 保存失敗:', error);
      setError(error instanceof Error ? error.message : 'Failed to save search');

      // 發生錯誤時仍嘗試獲取最新數據
      await fetchSavedSearches(true);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, sortSearches, isLoading, fetchSavedSearches, searchesRef]);

  const deleteSearch = useCallback(async (id: number) => {
    if (isLoading || !sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      console.debug('[deleteSearch] 開始刪除搜索 ID:', id);

      const response = await fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}&search_ids=${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        console.error('[deleteSearch] 刪除失敗，狀態碼:', response.status);
        throw new Error(`Failed to delete search: ${response.status}`);
      }

      console.debug('[deleteSearch] 刪除成功');

      // 直接從本地狀態中移除該項目，避免額外的 API 請求
      const updatedSearches = sortSearches(searchesRef.current.filter(s => s.id !== id));
      updateSearchesRef(updatedSearches);

      // 強制刷新確保UI更新
      setTimeout(() => {
        fetchSavedSearches(true);
      }, 100);
    } catch (error) {
      console.error('[deleteSearch] 刪除出錯:', error);
      setError(error instanceof Error ? error.message : 'Failed to delete search');
      // 發生錯誤時重新獲取數據
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  const reorderSearches = useCallback(async (startIndex: number, endIndex: number) => {
    if (isLoading || !sessionId) return;

    const newSearches = [...searchesRef.current];
    const [removed] = newSearches.splice(startIndex, 1);
    newSearches.splice(endIndex, 0, removed);
    const updatedSearches = newSearches.map((search, index) => ({ ...search, order: index }));
    const sortedSearches = sortSearches(updatedSearches);

    // 先更新本地狀態，提供即時反饋
    updateSearchesRef(sortedSearches);

    try {
      setIsLoading(true);
      await Promise.all(
        sortedSearches.map(search =>
          fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}&search_id=${search.id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order: search.order })
          })
        )
      );
    } catch (err) {
      // 發生錯誤時重新獲取數據
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sortSearches, sessionId, fetchSavedSearches, isLoading]);

  const clearSearches = useCallback(async () => {
    if (isLoading || !sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      // 只篩選非系統搜索
      const userSearchIds = searchesRef.current.filter(search => search.account !== '系統').map(search => search.id);
      if (userSearchIds.length === 0) {
        return;
      }

      console.debug('[clearSearches] 準備刪除的搜索IDs:', userSearchIds);

      // 逐個刪除，避免一次性刪除多個可能造成的問題
      for (const id of userSearchIds) {
        console.debug('[clearSearches] 刪除搜索 ID:', id);
        await fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}&search_ids=${id}`, {
          method: 'DELETE',
        });
      }

      console.debug('[clearSearches] 所有搜索已刪除');

      // 直接從本地狀態中移除非系統項目，避免額外的 API 請求
      const updatedSearches = sortSearches(searchesRef.current.filter(s => s.account === '系統'));
      updateSearchesRef(updatedSearches);

      // 強制刷新確保UI更新
      await fetchSavedSearches(true);
    } catch (error) {
      console.error('[clearSearches] 清空失敗:', error);
      setError(error instanceof Error ? error.message : 'Failed to clear searches');
      // 發生錯誤時重新獲取數據
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  const updateSearch = useCallback(async (id: number, updatedData: Partial<SavedSearch>) => {
    if (isLoading || !sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      await fetch(`${API_URL}/api/redis/saved-searches?session_id=${sessionId}&search_id=${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedData),
      });

      // 直接更新本地狀態，避免額外的 API 請求
      const updatedSearches = sortSearches(
        searchesRef.current.map(s => s.id === id ? { ...s, ...updatedData } : s)
      );
      updateSearchesRef(updatedSearches);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update search');
      // 發生錯誤時重新獲取數據
      await fetchSavedSearches(true);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  return {
    searches,
    isLoading,
    error,
    fetchSavedSearches,
    saveSearch,
    deleteSearch,
    reorderSearches,
    clearSearches,
    updateSearch,
  };
};
