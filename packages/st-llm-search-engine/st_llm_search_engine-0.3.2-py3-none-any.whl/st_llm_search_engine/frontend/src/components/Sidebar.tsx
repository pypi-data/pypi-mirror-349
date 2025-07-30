// src/components/Sidebar.tsx
import React, { useState, useEffect, useCallback, useRef } from "react";
import SidebarHeader from "./SidebarHeader";
import ButtonGroup from "./ButtonGroup";
import { SavedSearchList, SavedSearchListRef } from "./SavedSearchList";
import { SavedSearch } from "./SavedSearchList/types";
import SearchModal from "./SearchModal";

interface SidebarProps {
  title: string;
  apiUrl: string;
}

export default function Sidebar({ title, apiUrl }: SidebarProps) {
  console.debug('[Sidebar] 渲染組件');
  const [activeTab, setActiveTab] = useState<'filter' | 'settings'>('filter');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'create' | 'edit' | 'view'>('create');
  const [currentSearch, setCurrentSearch] = useState<SavedSearch | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [sessionIdFetched, setSessionIdFetched] = useState(false);
  // 新增狀態，追蹤保存搜索的結果
  const [saveResult, setSaveResult] = useState<{id: number, title: string} | null>(null);

  // 保存對 SavedSearchList 組件的引用
  const savedSearchListRef = useRef<SavedSearchListRef>(null);

  // 只在組件掛載時獲取 sessionId
  useEffect(() => {
    if (sessionIdFetched) return;

    const getSessionId = async () => {
      console.debug('[Sidebar] 開始獲取sessionId');
      let id = sessionStorage.getItem('session_id');
      if (id) {
        console.debug('[Sidebar] 從sessionStorage獲取到sessionId:', id);
        setSessionId(id);
        setSessionIdFetched(true);
      } else {
        try {
          // 從後端拿 session id
          console.debug('[Sidebar] 從API獲取sessionId');
          const response = await fetch(`${apiUrl}/api/session`);
          const data = await response.json();
          if (data.session_id) {
            console.debug('[Sidebar] API返回sessionId:', data.session_id);
            sessionStorage.setItem('session_id', data.session_id);
            setSessionId(data.session_id);
            setSessionIdFetched(true);
          }
        } catch (error) {
          console.error("[Sidebar] 獲取 session ID 失敗:", error);
        }
      }
    };

    getSessionId();
  }, [apiUrl, sessionIdFetched]);

  const handleSearchAction = useCallback((search: SavedSearch | null, mode: 'edit' | 'view' | 'create') => {
    console.debug('[Sidebar] handleSearchAction 觸發，mode:', mode, 'search:', search?.title);
    setCurrentSearch(search);
    setModalMode(mode);
    setModalOpen(true);
  }, []);

  const handleModalClose = useCallback(() => {
    console.debug('[Sidebar] 關閉模態框');
    setModalOpen(false);
  }, []);

  const handleSaveSearch = useCallback(async (data: any) => {
    console.debug('[Sidebar] 開始保存搜索:', data.title);

    if (!sessionId) {
      console.error('[Sidebar] sessionId不存在，無法保存');
      return;
    }

    if (!savedSearchListRef.current) {
      console.error('[Sidebar] savedSearchListRef不存在，無法保存');
      return;
    }

    setIsSaving(true);
    try {
      console.debug('[Sidebar] 保存模式:', modalMode);

      if (modalMode === 'create') {
        // 新增搜索 - 使用 SavedSearchList 的 handleSaveSearch 方法
        const searchData = {
          title: data.title,
          account: "使用者",
          order: 99, // 後端會自動調整
          query: {
            title: data.title,
            time: data.time,
            source: data.source,
            tags: data.tags,
            query: data.query,
            n: data.n,
            range: data.range
          }
        };

        console.debug('[Sidebar] 調用 handleSaveSearch，數據:', searchData.title);
        const result = await savedSearchListRef.current.handleSaveSearch(searchData);
        console.debug('[Sidebar] 保存結果:', result?.id);

        // 保存搜索結果
        if (result) {
          setSaveResult({
            id: result.id,
            title: result.title
          });
        }

        // 再次強制刷新，確保UI更新
        setTimeout(() => {
          if (savedSearchListRef.current) {
            console.debug('[Sidebar] 保存後延時強制刷新');
            savedSearchListRef.current.handleRefresh();
          }
        }, 500);

        // 第二次刷新，確保UI更新
        setTimeout(() => {
          if (savedSearchListRef.current) {
            console.debug('[Sidebar] 保存後第二次延時刷新');
            savedSearchListRef.current.handleRefresh();
          }
        }, 1000);
      } else if (modalMode === 'edit' && currentSearch) {
        // 編輯搜索 - 使用 SavedSearchList 的方法
        const updatedData = {
          title: data.title,
          query: {
            title: data.title,
            time: data.time,
            source: data.source,
            tags: data.tags,
            query: data.query,
            n: data.n,
            range: data.range
          }
        };

        console.debug('[Sidebar] 調用 handleUpdateSearch, ID:', currentSearch.id);
        await savedSearchListRef.current.handleUpdateSearch(currentSearch.id, updatedData);

        // 保存搜索結果
        setSaveResult({
          id: currentSearch.id,
          title: data.title
        });
      }

      setModalOpen(false);
      console.debug('[Sidebar] 保存完成，關閉模態框');
    } catch (error) {
      console.error("[Sidebar] 保存搜索失敗:", error);
    } finally {
      setIsSaving(false);
    }
  }, [modalMode, currentSearch, sessionId]);

  // 監聽保存結果，確保 UI 狀態一致
  useEffect(() => {
    if (saveResult && savedSearchListRef.current) {
      console.debug('[Sidebar] 檢測到保存結果變化:', saveResult);

      // 強制刷新
      savedSearchListRef.current.handleRefresh();

      // 清空保存結果
      setTimeout(() => {
        setSaveResult(null);
      }, 1000);
    }
  }, [saveResult]);

  return (
    <div style={{
      width: 288,
      height: "100vh",
      minHeight: "100vh",
      background: "#161616",
      color: "#FFFFFF",
      padding: "40px 24px 0 24px",
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-start",
      flexShrink: 0,
      boxSizing: "border-box",
      position: "fixed",
      left: 0,
      top: 0,
      bottom: 0,
      zIndex: 100,
    }}>
      <SidebarHeader title={title} />
      <div style={{ marginTop: 20, width: "100%", display: "flex", justifyContent: "center" }}>
        <ButtonGroup activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
      <div
        style={{
          background: 'rgba(34,34,34,0.7)',
          borderRadius: 8,
          padding: '16px 0',
          width: '100%',
          marginTop: 50,
          flex: 1,
          overflow: "auto",
          marginBottom: 0,
          paddingBottom: 24
        }}
      >
        {activeTab === 'filter' ? (
          sessionId && (
            <SavedSearchList
              ref={savedSearchListRef}
              apiUrl={apiUrl}
              sessionId={sessionId}
              onEdit={handleSearchAction}
            />
          )
        ) : (
          <div
            style={{
              color: '#aaa',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: 120,
              width: '100%',
              fontSize: 16,
              fontWeight: 500,
            }}
          >
            此功能還在開發中
          </div>
        )}
      </div>

      {modalOpen && (
        <SearchModal
          open={modalOpen}
          mode={modalMode}
          onClose={handleModalClose}
          onSave={handleSaveSearch}
          initialData={currentSearch ? {
            title: currentSearch.title,
            time: currentSearch.query.time,
            source: currentSearch.query.source,
            tags: currentSearch.query.tags,
            query: currentSearch.query.query,
            n: currentSearch.query.n,
            range: currentSearch.query.range
          } : null}
          isSaving={isSaving}
          apiUrl={apiUrl}
        />
      )}
    </div>
  );
}
