const DashboardPage = () => {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Aperçu général</h2>
      
      {/* Statistiques */}
      <div className="stats stats-vertical lg:stats-horizontal w-full shadow">
        <div className="stat">
          <div className="stat-figure text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block h-8 w-8 stroke-current"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          </div>
          <div className="stat-title">Total Élèves</div>
          <div className="stat-value">1,128</div>
          <div className="stat-desc">↗︎ 40 (4%)</div>
        </div>
        
        <div className="stat">
          <div className="stat-figure text-secondary">
             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block h-8 w-8 stroke-current"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <div className="stat-title">Total Enseignants</div>
          <div className="stat-value">73</div>
          <div className="stat-desc">↗︎ 5 (7%)</div>
        </div>
        
        <div className="stat">
          <div className="stat-figure text-secondary">
            <div className="avatar online">
              <div className="w-16 rounded-full">
                <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
              </div>
            </div>
          </div>
          <div className="stat-value">93.8%</div>
          <div className="stat-title">Taux de réussite</div>
          <div className="stat-desc text-secondary">31 matières restantes</div>
        </div>
      </div>

      {/* Activité Récente */}
      <div className="mt-8 card bg-base-100 shadow-xl">
        <div className="card-body">
            <h3 className="card-title">Activité Récente</h3>
            <div className="overflow-x-auto">
                <table className="table">
                    <tbody>
                    <tr><th>1</th><td>Nouvelle inscription : Mariam Cire Camara en 5ème Année.</td></tr>
                    <tr><th>2</th><td>Note ajoutée en Géographie pour Jacques Kaliva.</td></tr>
                    <tr><th>3</th><td>Paiement de scolarité reçu de Fanta Kourouma.</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;