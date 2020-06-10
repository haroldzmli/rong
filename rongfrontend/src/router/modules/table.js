/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/table',
  component: Layout,
  redirect: '/table/complex-table',
  name: 'table',
  meta: {
    title: '用户数表操作',
    icon: 'table'
  },
  children: [
    {
      path: 'user-info',
      component: () => import('@/views/table/user-info'),
      name: 'UserInfo',
      meta: { title: '用户信息' }
    },
    {
      path: 'dropzone',
      component: () => import('@/views/components-demo/dropzone'),
      name: 'DropzoneDemo',
      meta: { title: '上传数据' }
    },
    {
      path: 'user-map-data',
      component: () => import('@/views/table/user-map-data'),
      name: 'UserMapData',
      meta: { title: '用户数据' }
    },
    {
      path: 'user-map',
      component: () => import('@/views/table/user-map'),
      name: 'UserMap',
      meta: { title: '用户地图' }
    },
    {
      path: 'dynamic-table',
      component: () => import('@/views/table/dynamic-table/index'),
      name: 'DynamicTable',
      meta: { title: 'Dynamic Table' }
    },
    {
      path: 'drag-table',
      component: () => import('@/views/table/drag-table'),
      name: 'DragTable',
      meta: { title: 'Drag Table' }
    },
    {
      path: 'inline-edit-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'InlineEditTable',
      meta: { title: 'Inline Edit' }
    },
    {
      path: 'complex-table',
      component: () => import('@/views/table/complex-table'),
      name: 'ComplexTable',
      meta: { title: 'Complex Table' }
    }
  ]
}
export default tableRouter
